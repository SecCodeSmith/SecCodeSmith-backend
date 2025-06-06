import tempfile
from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Image

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ImageAPITests(APITestCase):
    def setUp(self):
        # create a dummy image so the endpoint has something to serve
        img_file = SimpleUploadedFile(
            "dummy.png", b"\x89PNG\r\n\x1a\n", content_type="image/png"
        )
        self.image = Image.objects.create(
            name="guild-alpha", alt="Guild crest", image=img_file
        )

    def test_get_image_success(self):
        url = reverse("core:image_detail", args=[self.image.name])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["name"], self.image.name)
        self.assertTrue(r.data["image"].endswith("dummy.png"))

    def test_get_image_not_found(self):
        url = reverse("core:image_detail", args=["does-not-exist"])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)
