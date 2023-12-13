from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.vendors import views

main_router = DefaultRouter()
main_router.register(r'', views.VendorViewSet, 'vendor-profile')

urlpatterns = [
    path('', include(main_router.urls)),
]
