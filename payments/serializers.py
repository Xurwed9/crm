from rest_framework import serializers
from .models import Payment, PaymentHistory
from django.db.models import Sum, Q


class PaymentListSerializer(serializers.ModelSerializer):

    student = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "student",
            "amount",
            "discount",
            "paid_date",
            "payment_method",
            "payment_method_display",
            "status",
            "status_display",
        )


class PaymentDetailSerializer(serializers.ModelSerializer):

    student = serializers.StringRelatedField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "student",
            "amount",
            "discount",
            "paid_date",
            "payment_method",
            "payment_method_display",
            "status",
            "status_display",
            "comment",
            "created_at",
            "updated_at",
        )


class PaymentCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "student",
            "amount",
            "discount",
            "paid_date",
            "payment_method",
            "status",
            "comment",
        )


class PaymentHistorySerializer(serializers.ModelSerializer):

    action_display = serializers.CharField(
        source="get_action_display",
        read_only=True,
    )

    class Meta:
        model = PaymentHistory
        fields = (
            "id",
            "action",
            "action_display",
            "changed_at",
            "old_data",
            "new_data",
        )


class StudentDebtSerializer(serializers.Serializer):

    student_id = serializers.IntegerField(
        source="id",
        read_only=True,
    )
    student_name = serializers.SerializerMethodField()
    total_fees = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    paid_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    total_discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    remaining = serializers.SerializerMethodField()

    def get_student_name(self, obj):
        return str(obj)

    def get_remaining(self, obj):
        total_fees = obj.total_fees or 0
        paid_amount = obj.paid_amount or 0
        total_discount = obj.total_discount or 0
        remaining = total_fees - paid_amount - total_discount
        return max(remaining, 0)
