from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Home",
    }
    return render(request, "minitube/home.html", context=context)


def contact(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Contact",
    }
    return render(request, "minitube/contact.html", context=context)


def gallery(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Gallery",
    }
    return render(request, "minitube/gallery.html", context=context)
