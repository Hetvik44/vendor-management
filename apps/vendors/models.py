import logging
from django.conf import settings
from django.db import models

from apps.base.models import Base

# logger = logging.getLogger(__name__)


class Vendor(Base):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile',
        help_text='User associated with vendor'
    )
    name = models.CharField(max_length=255, verbose_name="Vendor Name", help_text="Vendor's name.")
    contact_detail = models.TextField(verbose_name="Vendor's contact details", help_text="Vendor's contact details")
    vendor_code = models.CharField(
        verbose_name="Vendor's Code",
        max_length=32, unique=True, help_text="Vendor's unique code")
    on_time_delivery_rate = models.DecimalField(
        verbose_name="Vendor's delivery rate",
        max_digits=10, decimal_places=2,
        default=0, help_text="Vendor's on time delivery rate"
    )
    quality_rating_avg = models.DecimalField(
        verbose_name="Vendor's quality rating",
        max_digits=10, decimal_places=2,
        default=0, help_text="Vendor's avg quality rating"
    )
    average_response_time = models.DecimalField(
        verbose_name="Vendor's average response time", max_digits=10,
        decimal_places=2, default=0,
        help_text="Vendor's average response time"
    )
    fulfillment_rate = models.DecimalField(
        verbose_name="Vendor's fulfillment rate", max_digits=10,
        decimal_places=2, default=0,
        help_text="Vendor's order fulfillment rate"
    )

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "vm_vendor_profile"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"


class HistoricalPerformance(Base):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_performance')
    on_time_delivery_rate = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name="Vendor's delivery rate",
        help_text="Vendor's on time delivery rate"
    )
    quality_rating_avg = models.DecimalField(
        verbose_name="Vendor's quality rating", max_digits=10,
        decimal_places=2, default=0,
        help_text="Vendor's avg quality rating"
    )
    average_response_time = models.DecimalField(
        verbose_name="Vendor's average response time",
        max_digits=10, decimal_places=2, default=0,
        help_text="Vendor's average response time"
    )
    fulfillment_rate = models.DecimalField(
        verbose_name="Vendor's fulfillment rate", max_digits=10,
        decimal_places=2, default=0,
        help_text="Vendor's order fulfillment rate"
    )

    def __str__(self):
        return self.vendor.name

    class Meta:
        db_table = "vm_vendor_performance"
