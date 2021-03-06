# Generated by Django 3.0.5 on 2020-11-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0006_auto_20201107_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shipping',
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_price',
            field=models.IntegerField(blank=True, verbose_name='Shipping cost'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_price_stripe',
            field=models.CharField(blank=True, max_length=30, verbose_name='Shipping_price_ID'),
        ),
    ]
