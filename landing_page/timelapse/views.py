from django.shortcuts import render, get_object_or_404
from .forms import Landing_form
from .models import Service


def index(request):
    services = Service.objects.filter(available=True).order_by("-page_order")
    coming_soon = Service.objects.filter(coming_soon=True).order_by("page_order")

    context = {"services": services, "coming_soon": coming_soon}

    return render(request, "index.html", {"context": context})


def checkout(request, slug):
    selected_service = Service.objects.get(slug=slug)
    services = Service.objects.filter(available=True).order_by("-page_order")
    coming_soon = Service.objects.filter(coming_soon=True).order_by("page_order")

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
        for element in services:
            data.append({"textField": element.description})

        context = {
            "services": services,
            "servicesJSON": data,
            "coming_soon": coming_soon,
            "form": form,
            "selected_service": selected_service,
        }

    return render(request, "checkout.html", {"context": context})

