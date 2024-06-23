from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from .models import Photo, Video


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


def get_video_widget(request: HttpRequest, slug: str, widget_name: str) -> HttpResponse:
    video = get_object_or_404(Video, slug=slug)
    context = {"video": video}
    match widget_name:
        case "card":
            return render(request, "minitube/partials/video_card.html", context=context)
        case _:
            return HttpResponse(code=404)


def get_photo_widget(request: HttpRequest, slug: str, widget_name: str) -> HttpResponse:
    photo = get_object_or_404(Photo, slug=slug)
    context = {"photo": photo}
    match widget_name:
        case "card":
            return render(request, "minitube/partials/photo_card.html", context=context)
        case _:
            return HttpResponse(code=404)


def get_video(request: HttpRequest, slug: str) -> HttpResponse:
    video = get_object_or_404(Video, slug=slug)
    context = {
        "title": video.title,
        "video": video,
    }
    return render(request, "minitube/video.html", context=context)


def get_photo(request: HttpRequest, slug: str) -> HttpResponse:
    photo = get_object_or_404(Photo, slug=slug)
    context = {
        "title": photo.title,
        "photo": photo,
    }
    return render(request, "minitube/photo.html", context=context)
