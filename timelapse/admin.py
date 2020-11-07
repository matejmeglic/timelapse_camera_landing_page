from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductvAdmin(admin.ModelAdmin):
    list_display = (
        "page_order",
        "product",
        "slug",
        "price",
        "shipping_price",
        "available",
        "coming_soon",
        "description",
    )
    list_display_links = ("product",)
    ordering = ("page_order",)

