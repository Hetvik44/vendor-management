from django.apps import AppConfig


class PurchaseOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.purchase_orders'

    def ready(self):
        from apps.purchase_orders.signals import calculate_on_time_delivery_rate
