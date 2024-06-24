from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def validate_slug_is_unique(value: str) -> None:
    """Slugifies a value and tries to fetch a :model:`minitube.Media` child instance with that slug."""
    slug = slugify(value)
    all_medias = [subclass for subclass in Media.__subclasses__()]
    for media in all_medias:
        if media.objects.filter(slug=slug).exists():
            if media.objects.filter(slug=slug).first().title != value:
                raise ValidationError(_(f"'{value}' would generate a non-unique slug."))


class Comment(models.Model):
    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]

    user = models.ForeignKey("auth.User", on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=2048)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")
    object_id = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.created_on:%d-%m-%Y} - {self.user.username}"


class Media(models.Model):
    class Meta:
        abstract = False

    title = models.CharField(
        max_length=256, unique=True, validators=[validate_slug_is_unique]
    )
    slug = models.SlugField(max_length=256, unique=True, blank=True, editable=False)
    caption = models.CharField(max_length=256)
    source = models.FileField(storage=storages["bucket"])
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    @property
    def url(self) -> str:
        return self.source.url


class Video(Media):
    thumbnail = models.FileField(storage=storages["default"])


class Photo(Media):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    @property
    def dimensions(self) -> str:
        return f"{self.width}x{self.height}"
