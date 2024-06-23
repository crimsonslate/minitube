from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Media


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


def media(request: HttpRequest, media_slug: str) -> HttpResponse:
    media = get_object_or_404(Media, slug=media_slug)
    title = media.title if media.title else media.name

    context = {
        "title": title,
        "media": media,
    }
    return render(request, "minitube/media.html", context=context)
