from django.db import models
from students.models import Student
from accounts.models import User


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("transfer", "Transfer"),
        ("cheque", "Cheque"),
    )

    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    paid_date = models.DateField()

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-paid_date", "-created_at"]

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.get_status_display()})"


class PaymentHistory(models.Model):

    ACTION_CHOICES = (
        ("created", "Created"),
        ("updated", "Updated"),
        ("deleted", "Deleted"),
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="history",
    )

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_changes",
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
    )

    old_data = models.JSONField(
        null=True,
        blank=True,
    )

    new_data = models.JSONField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-changed_at"]
        verbose_name_plural = "payment histories"

    def __str__(self):
        return f"{self.payment} - {self.get_action_display()}"


class StudentDebt(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="debt",
    )

    total_fees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.student} - {self.total_fees}"
