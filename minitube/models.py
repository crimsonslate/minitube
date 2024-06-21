from django.core.files.storage import storages
from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.PROTECT)
    video = models.ForeignKey(
        "Video", related_name="comments", on_delete=models.PROTECT
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=2048)

    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.video.name} - {self.user} - {self.created_on:%d-%m-%Y} - "{self.text[:64]}"'


class Media(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=128)
    title = models.CharField(max_length=256, blank=True, null=True)
    caption = models.CharField(max_length=256)
    source = models.FileField(storage=storages["bucket"])

    def __str__(self) -> str:
        return self.name

    @property
    def url(self) -> str:
        return self.source.url


class Video(Media):
    # Alias of url
    @property
    def stream(self) -> str:
        return self.url

    duration = models.DurationField(blank=True, null=True, default=None)
