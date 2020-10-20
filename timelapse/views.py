from django.shortcuts import render, get_object_or_404
from .forms import Landing_form
from .models import Product
import stripe
import os
from django.http.response import JsonResponse, HttpResponse
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView


def index(request):
    products = Product.objects.filter(available=True).order_by("-page_order")
    coming_soon = Product.objects.filter(coming_soon=True).order_by("page_order")

    context = {"products": products, "coming_soon": coming_soon}

    return render(request, "index.html", {"context": context})


@csrf_exempt
def checkout(request, slug):
    selected_product = Product.objects.get(slug=slug)
    products = Product.objects.filter(available=True).order_by("-page_order")
    coming_soon = Product.objects.filter(coming_soon=True).order_by("page_order")

    if request.method == "POST":
        form = Landing_form(request.POST)

        if form.is_valid():
            current_order = form.save(commit=False)
            current_order.slug = slug
            current_order.save()

            context = {"current_order": current_order}

            return render(request, "stripe_page.html", {"context": context})

    else:
        form = Landing_form()
        form.slug = slug
        data = []

        for element in products:
            data.append(
                {
                    "product": element.product,
                    "price": element.price,
                    "shipping_price": element.shipping_price,
                    "description": element.description,
                }
            )

        context = {
            "products": products,
            "productsJSON": data,
            "coming_soon": coming_soon,
            "form": form,
            "selected_product": selected_product,
        }

    return render(request, "checkout.html", {"context": context})


def stripe_page(request):
    return render(request, "stripe_page.html", {})


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                customer_email="matej@matejmeglic.com",
                mode="payment",
                line_items=[
                    {
                        "name": "T-shirt",
                        "quantity": 1,
                        "currency": "usd",
                        "amount": "2000",
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelledView(TemplateView):
    template_name = "cancelled.html"


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = "whsec_TVXgZgjYDrryuUocfcMhUlhoj9p0C0sc"
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)
