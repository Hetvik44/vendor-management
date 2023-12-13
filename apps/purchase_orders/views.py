import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.purchase_orders import models
from apps.purchase_orders import serializers
from apps.purchase_orders.functions import get_unhandled_message

logger = logging.getLogger(__name__)

acknowledge_response = openapi.Response(
    'Response Description', serializers.PurchaseOrderSerializer
)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    list:
    Get list of Purchase Order.

    You list of Purchase Order using this endpoint

    create:
    Create a Purchase Order.

    You can create Purchase Order using this endpoint

    update:
    Update Purchase Order

    You can update Purchase Order using this endpoint

    retrieve:
    Get a specific Purchase Order

    You can get a specific Purchase Order using this endpoint

    delete:
    Delete Purchase Order

    You can delete Purchase Order using this endpoint
    """
    permission_classes = (permissions.IsAuthenticated, )
    filterset_fields = ('vendor__name', 'status')

    def get_serializer_class(self):
        return serializers.PurchaseOrderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.PurchaseOrder.objects.all()
        return models.PurchaseOrder.objects.filter(vendor__user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        logger.info("Creating Purchase order for User: %s", request.user)
        request_data = request.data
        ser = serializers.PurchaseOrderSerializer(data=request_data, context={"request": self.request})
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
        ser.save(vendor=self.request.user.vendor_profile)
        return Response(data=ser.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting purchase order for User: %s", request.user)
        super().destroy(request, *args, **kwargs)

        return Response(
            {
                "message": "Purchase Order deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        responses={200: acknowledge_response}, request_body=serializers.AcknowlegdeSerializer,
        operation_summary="Update acknowledge",
        operation_description="You can update the purchase order acknowledge date"
    )
    @action(detail=True, methods=['post'], url_name='acknowledge', url_path='acknowledge')
    def update_acknowledge(self, request, pk=None):
        try:
            logger.info(
                "Update acknowledge called by %s for purchase order: %s", request.user.username, pk
            )
            purchase_order = self.get_object()
            purchase_order.acknowledgement_date = request.data.get('acknowledgement_date')
            purchase_order.save()
            return Response(
                serializers.PurchaseOrderSerializer(instance=purchase_order).data,
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            logger.critical("Caught exception in {}".format(__file__), exc_info=True)
            return Response(
                {"message": get_unhandled_message(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

