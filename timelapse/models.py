from django.db import models
import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# comment
class Product(models.Model):
    page_order = models.IntegerField("Page order", default=50)
    product = models.CharField("Product", max_length=30)
    slug = models.SlugField("Slug")
    description = models.TextField("Description")
    price = models.IntegerField("Price")
    shipping_price = models.IntegerField("Shipping cost", default=0)
    available = models.BooleanField("Available", default=False)
    coming_soon = models.BooleanField("Coming soon", default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-available", "product")

    def __str__(self):
        return self.product


class Order(models.Model):
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )
    quantity = models.IntegerField("Quantity", default=1)
    name = models.CharField("Name", max_length=30)
    email = models.EmailField("Email")
    message = models.TextField("Message", max_length=300, blank=True, null=True)
    GDPR = models.BooleanField("Allow communication", default=True)
    order_delivered = models.BooleanField("Was order completed", default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ("order_delivered", "timestamp")

    def __str__(self):
        return self.name
