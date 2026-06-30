from django.db import models
from django.utils.translation import gettext_lazy as _

from students.models import Student
from accounts.models import User


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ("cash", _("Cash")),
        ("card", _("Card")),
        ("transfer", _("Transfer")),
        ("cheque", _("Cheque")),
    )

    STATUS_CHOICES = (
        ("paid", _("Paid")),
        ("pending", _("Pending")),
        ("cancelled", _("Cancelled")),
        ("refunded", _("Refunded")),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Student"),
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Amount"),
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Discount"),
    )

    paid_date = models.DateField(
        verbose_name=_("Paid date"),
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name=_("Payment method"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("Comment"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-paid_date", "-created_at"]

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.get_status_display()})"


class PaymentHistory(models.Model):

    ACTION_CHOICES = (
        ("created", _("Created")),
        ("updated", _("Updated")),
        ("deleted", _("Deleted")),
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name=_("Payment"),
    )

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        verbose_name=_("Action"),
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_changes",
        verbose_name=_("Changed by"),
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Changed at"),
    )

    old_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Old data"),
    )

    new_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("New data"),
    )

    class Meta:
        verbose_name = _("Payment history")
        verbose_name_plural = _("Payment histories")
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.payment} - {self.get_action_display()}"


class StudentDebt(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="debt",
        verbose_name=_("Student"),
    )

    total_fees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Total fees"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        verbose_name = _("Student debt")
        verbose_name_plural = _("Student debts")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.student} - {self.total_fees}"
