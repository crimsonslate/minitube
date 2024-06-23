from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("gallery/", views.gallery, name="gallery"),
    path("video/<str:slug>/", views.get_video, name="get video"),
    path(
        "video/<str:slug>/<str:widget_name>/",
        views.get_video_widget,
        name="get video widget",
    ),
    path("photo/<str:slug>/", views.get_photo, name="get photo"),
    path(
        "photo/<str:slug>/<str:widget_name>/",
        views.get_photo_widget,
        name="get photo widget",
    ),
]
