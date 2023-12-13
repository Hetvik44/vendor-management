from rest_framework import serializers

from apps.base.serializers import BaseSerializer
from apps.purchase_orders.models import PurchaseOrder
from apps.vendors.models import Vendor
from apps.vendors.serializers import VendorSerializer


class PurchaseOrderSerializer(BaseSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            'id', 'po_number', 'vendor', 'delivery_date', 'items', 'quantity',
            'status', 'quality_rating', 'issue_date', 'acknowledgement_date'
        )
        read_only_fields = ('vendor', )

    def validate(self, data):
        data = super().validate(data)
        vendor = Vendor.objects.filter(user=self.context.get('request', {}).user)
        if not vendor.exists():
            raise serializers.ValidationError("Vendor not created for this user")
        return data


class AcknowlegdeSerializer(serializers.Serializer):
    acknowledgement_date = serializers.DateTimeField(help_text="Vendors to acknowledge POs.", required=True)
