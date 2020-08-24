from django.contrib import admin
from . import models


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("page_order", "service", "available", "description")
    ordering = ("page_order",)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "order_delivered",
        "service",
        "name",
        "email",
        "GDPR",
        "message",
    )
    ordering = ("-timestamp", "order_delivered")

