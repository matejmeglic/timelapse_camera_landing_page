from django.db import models


class Product(models.Model):
    page_order = models.IntegerField("Page order", default=50)
    product = models.CharField("Product", max_length=30)
    slug = models.SlugField("Slug")
    description = models.TextField("Description")
    price = models.IntegerField("Price")
    price_stripe = models.CharField("Price_ID", max_length=30, default="")
    price_tax = models.IntegerField("Price tax")
    price_tax_stripe = models.CharField("Price_tax_ID", max_length=30, default="")
    shipping_price = models.IntegerField("Shipping cost", null=True, blank=True)
    shipping_price_stripe = models.CharField(
        "Shipping_price_ID", max_length=30, null=True, blank=True
    )
    shipping_tax = models.IntegerField("Shipping tax", null=True, blank=True)
    shipping_tax_stripe = models.CharField(
        "Shipping_tax_ID", max_length=30, null=True, blank=True
    )
    available = models.BooleanField("Available", default=False)
    coming_soon = models.BooleanField("Coming soon", default=False)
    asdf = models.BooleanField("asdf", default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-available", "product")

    def __str__(self):
        return self.product

