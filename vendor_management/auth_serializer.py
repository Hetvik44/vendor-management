from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.vendors.serializers import VendorSerializer


class VendorTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['access_token'] = data['access']
        data['refresh_token'] = data['refresh']
        # data['vendor'] = VendorSerializer(instance=self.user.vendor_profile).data
        del data['access']
        del data['refresh']
        return data


class VendorTokenObtainPairView(TokenObtainPairView):
    serializer_class = VendorTokenObtainPairSerializer
