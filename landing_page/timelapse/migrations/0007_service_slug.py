# Generated by Django 3.1 on 2020-08-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0006_service_page_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='slug',
            field=models.SlugField(default=1, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]
