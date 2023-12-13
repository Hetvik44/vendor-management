from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from vendor_management.auth_serializer import VendorTokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="Vendor Management API",
      default_version='v1',
      description="All the endpoints of the Vendor Management Backend",
   ),
   public=True,
   permission_classes=(AllowAny,),
   url=settings.BASE_API_URL,
)
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),

    path('api/auth/login/', VendorTokenObtainPairView.as_view(), name='login'),
    path('api/auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/vendors/', include(('apps.vendors.urls', "vendors"), namespace="vendors")),
    path('api/purchase-orders/', include(('apps.purchase_orders.urls', "purchase_orders"), namespace="purchase_orders")),

]
