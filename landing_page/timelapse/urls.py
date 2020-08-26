from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/<str:slug>/", views.checkout, name="checkout"),
]
