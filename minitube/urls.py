from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("gallery/", views.gallery, name="gallery"),
    path("<str:media_slug>/", views.media, name="media"),
]
