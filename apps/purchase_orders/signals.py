from django.db import transaction
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.purchase_orders.models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        total_completed_purchases = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed'
        )
        total_completed_purchases_count = total_completed_purchases.count()
        completed_purchases_count = total_completed_purchases.filter(delivery_date__lte=instance.delivery_date).count()

        on_time_delivery_rate = (
            completed_purchases_count / total_completed_purchases_count
        ) if total_completed_purchases_count > 0 else 0

        new_average_quality_rating = 0
        if instance.quality_rating:
            completed_purchases = total_completed_purchases.exclude(quality_rating=0)

            if completed_purchases.count() > 0:
                new_average_quality_rating = (completed_purchases.aggregate(Avg('quality_rating'))['quality_rating__avg'])

        with transaction.atomic():
            vendor = instance.vendor
            vendor.on_time_delivery_rate = round(on_time_delivery_rate, 2)
            vendor.quality_rating_avg = round(new_average_quality_rating, 2)
            vendor.save()

    if instance.acknowledgement_date:
        total_purchases = PurchaseOrder.objects.filter(
            vendor=instance.vendor
        )

        total_purchases_count = total_purchases.count()

        if total_purchases_count > 0:
            response_times = [
                round((po.acknowledgement_date - po.issue_date).total_seconds()/60)
                for po in total_purchases.filter(acknowledgement_date__isnull=False)
            ]
            average_response_time = sum(response_times) / total_purchases_count
        else:
            average_response_time = None

        with transaction.atomic():
            vendor = instance.vendor
            vendor.average_response_time = average_response_time
            vendor.save()
