from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductvAdmin(admin.ModelAdmin):
    list_display = (
        "page_order",
        "product",
        "slug",
        "available",
        "coming_soon",
        "description",
    )
    list_display_links = ("product",)
    ordering = ("page_order",)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "order_delivered",
        "product",
        "name",
        "email",
        "GDPR",
        "message",
    )
    ordering = ("-timestamp", "order_delivered")

