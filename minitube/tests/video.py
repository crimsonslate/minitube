import io

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils.text import slugify

from minitube.models import Video


def generate_test_video_file() -> ContentFile:
    video_content = io.BytesIO(b"test video content")
    return ContentFile(video_content.getvalue(), "test_video.mp4")


def generate_test_thumbnail() -> ContentFile:
    content = io.BytesIO(b"thumbnail content")
    return ContentFile(content.getvalue(), "thumbnail.png")


class VideoModelTestCase(TestCase):
    def setUp(self):
        test_source = generate_test_video_file()
        test_thumbnail = generate_test_thumbnail()
        self.test_video = Video.objects.create(
            title="Test Video",
            caption="Test Caption",
            source=test_source,
            thumbnail=test_thumbnail,
        )

    def test_video_automatically_creates_slug(self) -> None:
        """Succeeds if the test video generates an accessible slug."""
        good_slug = slugify("Test Video")

        # Fails if the slug wasn't set at all
        self.assertIsNot(self.test_video.slug, None)
        # Fails if the slug wasn't set according to the title
        self.assertEqual(self.test_video.slug, good_slug)

    def test_video_is_accessible_via_slug(self) -> None:
        """Succeeds if the test video can be accessed via its slug."""
        good_slug = slugify("Test Video")

        response = self.client.get(f"/{good_slug}/")
        # Fails if a client cannot access the video via slug
        self.assertEqual(response.status_code, 200)

    def test_cannot_create_videos_with_similar_titles(self) -> None:
        """Succeeds if ValidationError is raised before a bad title could be written to the database."""
        bad_test_source = generate_test_video_file()
        bad_test_thumbnail = generate_test_thumbnail()
        bad_test_video = Video.objects.create(
            title="good slug",
            caption="I would definitely break a database.",
            source=bad_test_source,
            thumbnail=bad_test_thumbnail,
        )
        with self.assertRaisesMessage(
            ValidationError, "'test video' would generate a non-unique slug."
        ):
            bad_test_video.title = "test video"
            bad_test_video.full_clean()
