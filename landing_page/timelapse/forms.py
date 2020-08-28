from django import forms
from django.forms import ModelForm
from .models import Order, Product


class Landing_form(ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(available=True).order_by("-page_order")
    )

    class Meta:
        model = Order
        exclude = ("order_delivered", "timestamp")

