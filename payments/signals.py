from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Payment, PaymentHistory


@receiver(post_save, sender=Payment)
def log_payment_save(sender, instance, created, **kwargs):

    action = "created" if created else "updated"

    old_data = None

    if not created:
        try:
            old_instance = Payment.objects.get(pk=instance.pk)
            old_data = {
                "amount": str(old_instance.amount),
                "discount": str(old_instance.discount),
                "paid_date": str(old_instance.paid_date),
                "payment_method": old_instance.payment_method,
                "status": old_instance.status,
                "comment": old_instance.comment,
            }
        except Payment.DoesNotExist:
            old_data = None

    new_data = {
        "amount": str(instance.amount),
        "discount": str(instance.discount),
        "paid_date": str(instance.paid_date),
        "payment_method": instance.payment_method,
        "status": instance.status,
        "comment": instance.comment,
    }

    PaymentHistory.objects.create(
        payment=instance,
        action=action,
        old_data=old_data if not created else None,
        new_data=new_data,
    )


@receiver(post_delete, sender=Payment)
def log_payment_delete(sender, instance, **kwargs):

    deleted_data = {
        "amount": str(instance.amount),
        "discount": str(instance.discount),
        "paid_date": str(instance.paid_date),
        "payment_method": instance.payment_method,
        "status": instance.status,
        "comment": instance.comment,
    }

    PaymentHistory.objects.create(
        payment=instance,
        action="deleted",
        old_data=deleted_data,
        new_data=None,
    )
