from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.db.models import Sum, Q, Value, OuterRef, Subquery, DecimalField
from django.db.models.functions import Coalesce

from students.models import Student
from .models import Payment, PaymentHistory, StudentDebt
from .serializers import (
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentCreateUpdateSerializer,
    PaymentHistorySerializer,
    StudentDebtSerializer,
)
from .permissions import (
    CanViewPayment,
    CanCreatePayment,
    CanEditPayment,
    CanDeletePayment,
    CanViewPaymentHistory,
)


class PaymentListAPIView(ListAPIView):

    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated, CanViewPayment]
    filter_backends = [SearchFilter]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "payment_method",
        "status",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Payment.objects.select_related(
            "student",
            "student__user",
        )

        if user.role == "admin":
            return queryset

        if user.role == "student":
            return queryset.filter(student__user=user)

        return Payment.objects.none()


class PaymentDetailAPIView(RetrieveAPIView):

    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAuthenticated, CanViewPayment]

    def get_queryset(self):

        return Payment.objects.select_related(
            "student",
            "student__user",
        )


class PaymentCreateAPIView(CreateAPIView):

    serializer_class = PaymentCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanCreatePayment]


class PaymentUpdateAPIView(UpdateAPIView):

    serializer_class = PaymentCreateUpdateSerializer
    permission_classes = [IsAuthenticated, CanEditPayment]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Payment.objects.select_related(
            "student",
            "student__user",
        )


class PaymentDeleteAPIView(DestroyAPIView):

    permission_classes = [IsAuthenticated, CanDeletePayment]

    def get_queryset(self):
        return Payment.objects.select_related(
            "student",
            "student__user",
        )

    def destroy(self, request, *args, **kwargs):

        payment = self.get_object()
        payment.delete()

        return Response(
            {"detail": _("Payment deleted successfully.")},
            status=status.HTTP_200_OK,
        )


class PaymentHistoryListAPIView(ListAPIView):

    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated, CanViewPaymentHistory]

    def get_queryset(self):

        return PaymentHistory.objects.filter(
            payment_id=self.kwargs["payment_pk"],
        ).select_related("payment")


class StudentDebtListAPIView(ListAPIView):

    serializer_class = StudentDebtSerializer
    permission_classes = [IsAuthenticated, CanViewPayment]

    def get_queryset(self):

        user = self.request.user

        total_fees_subq = StudentDebt.objects.filter(
            student=OuterRef("pk"),
        ).values("total_fees")[:1]

        students = Student.objects.annotate(
            total_fees=Coalesce(
                Subquery(total_fees_subq),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            paid_amount=Coalesce(
                Sum(
                    "payments__amount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            total_discount=Coalesce(
                Sum(
                    "payments__discount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )

        if user.role == "admin":
            return students

        if user.role == "student":
            return students.filter(user=user)

        return Student.objects.none()


class StudentDebtDetailAPIView(RetrieveAPIView):

    serializer_class = StudentDebtSerializer
    permission_classes = [IsAuthenticated, CanViewPayment]

    def get_object(self):

        user = self.request.user

        total_fees_subq = StudentDebt.objects.filter(
            student=OuterRef("pk"),
        ).values("total_fees")[:1]

        student = Student.objects.annotate(
            total_fees=Coalesce(
                Subquery(total_fees_subq),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            paid_amount=Coalesce(
                Sum(
                    "payments__amount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            total_discount=Coalesce(
                Sum(
                    "payments__discount",
                    filter=Q(payments__status="paid"),
                ),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        ).get(pk=self.kwargs["student_id"])

        if user.role == "student" and student.user != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                _("You can only view your own debt.")
            )

        return student
