# Generated by Django 3.0.5 on 2020-11-07 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0005_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shipping',
            field=models.BooleanField(blank=True, default=False, verbose_name='Include Shipping'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_price',
            field=models.IntegerField(blank=True, default=0, verbose_name='Shipping cost'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_price_stripe',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Shipping_price_ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_tax',
            field=models.IntegerField(blank=True, verbose_name='Shipping tax'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_tax_stripe',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Shipping_tax_ID'),
        ),
    ]
