# Generated by Django 5.0 on 2023-12-09 13:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='Last Updated Date')),
                ('po_number', models.CharField(max_length=10, verbose_name='- Unique number identifying the PO')),
                ('delivery_date', models.DateTimeField(verbose_name='Expected or actual delivery date of the order')),
                ('items', models.JSONField(default=dict, verbose_name='Details of items ordered')),
                ('quantity', models.IntegerField(verbose_name='- Total quantity of items in the PO')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=10, verbose_name='Current status of the PO')),
                ('quality_rating', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Rating given to the vendor for this PO')),
                ('issue_date', models.DateTimeField(verbose_name='Timestamp when the PO was issued to the vendor')),
                ('acknowledgement_date', models.DateTimeField(blank=True, null=True, verbose_name='Timestamp when the vendor acknowledged the PO')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_related', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated_related', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_purchase_order', to='vendors.vendor')),
            ],
            options={
                'verbose_name': 'Purchase Order',
                'verbose_name_plural': 'Purchase Orders',
                'db_table': 'vm_vendor_purchase_order',
            },
        ),
    ]
