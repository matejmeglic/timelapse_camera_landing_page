from django.shortcuts import render, get_object_or_404
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
    coming_soon = Product.objects.filter(coming_soon=True).order_by("-page_order")

    context = {"products": products, "coming_soon": coming_soon}

    return render(request, "index.html", {"context": context})


@csrf_exempt
def checkout(request, slug):
    selected_product = Product.objects.get(slug=slug)
    products = Product.objects.filter(available=True).order_by("-page_order")
    coming_soon = Product.objects.filter(coming_soon=True).order_by("page_order")

    data = []

    for element in products:
        data.append(
            {
                "product": element.product,
                "slug": element.slug,
                "price": element.price,
                "shipping_price": element.shipping_price,
                "description": element.description,
            }
        )

    context = {
        "products": products,
        "productsJSON": data,
        "coming_soon": coming_soon,
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

        # Create Stripe lineItems (add shipping+tax)
        orderedProduct = Product.objects.filter(slug=request.GET.get("slug"))[0]
        items = [{}]

        print(request)
        print(request.GET.get("quantity"))

        if orderedProduct.shipping_price > 0:
            items = [
                {
                    "price": orderedProduct.price_stripe,
                    "quantity": request.GET.get("quantity"),
                    "tax_rates": [orderedProduct.price_tax_stripe],
                },
                {
                    "price": orderedProduct.shipping_price_stripe,
                    "quantity": 1,
                    "tax_rates": [orderedProduct.shipping_tax_stripe],
                },
            ]
        else:
            items = [
                {
                    "price": orderedProduct.price_stripe,
                    "quantity": request.GET.get("quantity"),
                    "tax_rates": [orderedProduct.price_tax_stripe],
                }
            ]

        try:
            # Create new Stripe Checkout Session for the order

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                billing_address_collection="required",
                mode="payment",
                line_items=items,
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelledView(TemplateView):
    template_name = "cancelled.html"


# NOT USED
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = os.getenv("STRIPE_WEBHOOK")
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
