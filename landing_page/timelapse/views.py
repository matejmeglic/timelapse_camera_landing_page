from django.shortcuts import render, get_object_or_404
from .forms import Landing_form
from .models import Service


def index(request):
    services = Service.objects.filter(available=True)

    return render(request, "index.html", {"services": services})


def checkout(request, serviceid):
    URLservice = Service.objects.get(id=serviceid)
    if request.method == "POST":
        form = Landing_form(request.POST)

        if form.is_valid():
            current_order = form.save(commit=False)
            current_order.service = URLservice
            current_order.save()

            return render(
                request, "confirmation.html", {"current_order": current_order}
            )

    else:
        form = Landing_form()

        form.URLservice = URLservice

    return render(request, "checkout.html", {"form": form})

