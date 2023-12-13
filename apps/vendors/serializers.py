from rest_framework import serializers

from apps.base.serializers import BaseSerializer
from apps.vendors.models import Vendor


class VendorSerializer(BaseSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Vendor
        fields = (
            'id', 'user', 'name', 'contact_detail', 'vendor_code',
        )

    def validate(self, data):
        data = super().validate(data)
        vendor = Vendor.objects.filter(user=self.context.get('request', {}).user)
        if vendor.exists():
            raise serializers.ValidationError("Vendor already created")
        return data


class VendorPerformanceSerializer(BaseSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Vendor
        fields = (
            'id', 'user', 'name', 'contact_detail', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg',
            'average_response_time', 'fulfillment_rate',
        )
        read_only_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate',)
