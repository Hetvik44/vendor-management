import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.purchase_orders.functions import get_unhandled_message
from apps.vendors.models import Vendor
from apps.vendors.serializers import VendorSerializer, VendorPerformanceSerializer

logger = logging.getLogger(__name__)

acknowledge_response = openapi.Response(
    'Response Description', VendorPerformanceSerializer
)


class VendorViewSet(viewsets.ModelViewSet):
    """
    list:
    Get a Vendor Profile.

    You only get your profile using this endpoint

    create:
    Create a Vendor Profile.

    You can create vendor profile using this endpoint

    update:
    Update Vendor Profile

    You can update vendor's profile using this endpoint

    retrieve:
    Get a specific vendor's profile

    You can get a specific vendor's profile using this endpoint

    delete:
    Delete vendor profile

    You can delete vendor's profile using this endpoint
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return VendorSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Vendor.objects.all()
        return Vendor.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        logger.info("Creating vendor profile for User: %s", request.user)
        request_data = request.data
        ser = VendorSerializer(data=request_data, context={'request': self.request})
        valid, message = ser.validate_serializer()
        if not valid:
            logger.error(
                "Failed to create case. User: %s, error: %s", request.user, message
            )
            return Response(
                {
                    "message": "Data validation Failed. error: %s" % message,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        ser.save(user=self.request.user)
        return Response(data=ser.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting vendor profile for User: %s", request.user)
        super().destroy(request, *args, **kwargs)

        return Response(
            {
                "message": "Vendor deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        responses={200: acknowledge_response},
        operation_description="You can get a vendor's performance using this endpoint",
        operation_summary="Get Vendor Performance")
    @action(detail=True, methods=['get'], url_name='performance', url_path='performance')
    def get_performance(self, request, pk=None):
        try:
            logger.info("Getting vendor performance for User: %s", request.user)
            purchase_order = self.get_object()
            return Response(
                VendorPerformanceSerializer(instance=purchase_order).data,
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response(
                {"message": get_unhandled_message(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
