# Generated by Django 3.0.5 on 2020-11-08 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0008_auto_20201107_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shipping_price',
            field=models.IntegerField(default=0, verbose_name='Shipping cost'),
        ),
    ]
