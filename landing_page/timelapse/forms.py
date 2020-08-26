from django import forms
from django.forms import ModelForm
from .models import Order, Service


class Landing_form(ModelForm):
    # service = forms.ModelChoiceField(queryset=Service.objects.filter(available=True))

    class Meta:
        model = Order
        exclude = ("order_delivered", "timestamp")

