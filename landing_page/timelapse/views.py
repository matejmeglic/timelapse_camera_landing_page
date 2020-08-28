from django.shortcuts import render, get_object_or_404
from .forms import Landing_form
from .models import Product


def index(request):
    products = Product.objects.filter(available=True).order_by("-page_order")
    coming_soon = Product.objects.filter(coming_soon=True).order_by("page_order")

    context = {"products": products, "coming_soon": coming_soon}

    return render(request, "index.html", {"context": context})


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

            return render(
                request, "confirmation.html", {"current_order": current_order}
            )

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

