from django.urls import path
from .views import (
    PaymentListAPIView,
    PaymentDetailAPIView,
    PaymentCreateAPIView,
    PaymentUpdateAPIView,
    PaymentDeleteAPIView,
    PaymentHistoryListAPIView,
    StudentDebtListAPIView,
    StudentDebtDetailAPIView,
)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("payments/<int:pk>/", PaymentDetailAPIView.as_view(), name="payment-detail"),
    path("payments/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payment-update"),
    path("payments/<int:pk>/delete/", PaymentDeleteAPIView.as_view(), name="payment-delete"),
    path(
        "payments/<int:payment_pk>/history/",
        PaymentHistoryListAPIView.as_view(),
        name="payment-history",
    ),
    path("debts/", StudentDebtListAPIView.as_view(), name="debt-list"),
    path("debts/<int:student_id>/", StudentDebtDetailAPIView.as_view(), name="debt-detail"),
]
