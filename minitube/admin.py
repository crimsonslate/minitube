from django.contrib import admin

from .models import Comment, Photo, Video

admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(Photo)
