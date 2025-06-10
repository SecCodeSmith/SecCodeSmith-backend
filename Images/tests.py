import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock

from Images.models import Image

class ImagePropsTests(APITestCase):
    def setUp(self):
        # Create a sample image file
        self.sample_file = SimpleUploadedFile(
            name='test.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        # Create a valid image entry
        self.image = Image.objects.create(
            name='existing',
            alt='An existing image',
            image=self.sample_file
        )
        # Helper to build detail URLs
        self.detail_url = lambda name: reverse('image:image_list', kwargs={'name': name})

    def tearDown(self):
        self.image.image.delete(save=False)
        self.image.delete()



    def test_existing_image_returns_props(self):
        url = self.detail_url(self.image.name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
        self.assertIn('name', response.data)
        self.assertIn('alt', response.data)
        self.assertEqual(response.data['name'], self.image.name)
        self.assertEqual(response.data['alt'], self.image.alt)

    def test_nonexistent_image_returns_404(self):
        url = self.detail_url('missing')
        response = self.client.get(url)
        payload = json.loads(response.text)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(payload, {'error': 'Image not found'})

    def test_multiple_objects_returns_400(self):
        # Create duplicates to trigger MultipleObjectsReturned
        img1 = Image.objects.create(name='dup', alt='First', image=self.sample_file)
        img2 = Image.objects.create(name='dup', alt='Second', image=self.sample_file)
        url = self.detail_url('dup')
        response = self.client.get(url)
        payload = json.loads(response.text)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(payload, {'error': 'Problem with database'})

        img1.image.delete(save=False)
        img2.image.delete(save=False)
        img1.delete()
        img2.delete()