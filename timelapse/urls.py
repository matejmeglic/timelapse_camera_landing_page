from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/<str:slug>/", views.checkout, name="checkout"),
    path("stripe_page/", views.stripe_page, name="stripe_page"),
    path("config/", views.stripe_config),
    path("create-checkout-session/", views.create_checkout_session),
    path("success/", views.SuccessView.as_view()),
    path("cancelled/", views.CancelledView.as_view()),
    path("webhook/", views.stripe_webhook),  # new
]
