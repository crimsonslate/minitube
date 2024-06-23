from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def validate_slug_is_unique(value: str) -> None:
    """Slugifies a value and tries to fetch a :model:`minitube.Media` instance with that slug."""
    slug = slugify(value)
    try:
        media = Media.objects.get(slug=slug)
        raise ValidationError(_(f"'{value}' would generate a non-unique slug."))
    except Media.DoesNotExist:
        pass


class Comment(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.PROTECT)
    media = models.ForeignKey(
        "Media", related_name="comments", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=2048)

    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.media.name} - {self.user} - {self.created_on:%d-%m-%Y} - "{self.text[:64]}"'


class Media(models.Model):
    class Meta:
        verbose_name_plural = "media"

    title = models.CharField(
        max_length=256, unique=True, validators=[validate_slug_is_unique]
    )
    slug = models.SlugField(max_length=256, unique=True, blank=True, editable=False)
    caption = models.CharField(max_length=256)
    source = models.FileField(storage=storages["bucket"])
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    @property
    def url(self) -> str:
        return self.source.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Video(Media):
    thumbnail = models.FileField(storage=storages["staticfiles"])


class Photo(Media):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    @property
    def dimensions(self) -> str:
        return f"{self.width}x{self.height}"
