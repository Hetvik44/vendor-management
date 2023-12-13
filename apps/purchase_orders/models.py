import logging
from django.conf import settings
from django.db import models, transaction
from django.db.models import JSONField

from apps.base.models import Base

# logger = logging.getLogger(__name__)
from apps.purchase_orders.constant import PurchaseOrderStatus
from apps.vendors.models import Vendor


class PurchaseOrder(Base):
    po_number = models.CharField(max_length=10, help_text="PO Unique number identifying")
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE,
        help_text="Vendor associated with PO"
    )
    delivery_date = models.DateTimeField(help_text="Expected or actual delivery date of the order")
    items = JSONField(default=dict, help_text="Details of items ordered")
    quantity = models.IntegerField(help_text="Total quantity of items in the PO")
    status = models.CharField(
        choices=PurchaseOrderStatus.choices(), default=PurchaseOrderStatus.PENDING,
        max_length=10,
        help_text="Current status of the PO"
    )
    quality_rating = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Rating given to the vendor for this PO"
    )
    issue_date = models.DateTimeField(
        verbose_name='Timestamp when the PO was issued to the vendor',
        help_text="Timestamp when the PO was issued to the vendor"
    )
    acknowledgement_date = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp when the vendor acknowledged the PO"
    )
    __original_status = None

    def __str__(self):
        return self.po_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.status != self.__original_status:
                total_orders = PurchaseOrder.objects.filter(vendor=self.vendor)
                successfully_fulfilled_orders_count = total_orders.filter(status='completed').count()
                total_orders_count = total_orders.count()

                if total_orders_count > 0:
                    fulfillment_rate = successfully_fulfilled_orders_count / total_orders_count
                else:
                    fulfillment_rate = 0

                with transaction.atomic():
                    self.vendor.fulfillment_rate = fulfillment_rate
                    self.vendor.save()
            super().save(*args, **kwargs)

    class Meta:
        db_table = "vm_vendor_purchase_order"
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"
