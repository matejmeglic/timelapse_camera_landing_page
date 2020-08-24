from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/<int:serviceid>/", views.checkout, name="checkout"),
]
