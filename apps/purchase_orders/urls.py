from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.purchase_orders import views

main_router = DefaultRouter()
main_router.register(r'', views.PurchaseOrderViewSet, 'vendor-purchase-order')

urlpatterns = [
    path('', include(main_router.urls)),
]
