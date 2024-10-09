# Generated by Django 5.1.1 on 2024-10-03 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_filter_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='filter_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_app.filter_price'),
        ),
    ]