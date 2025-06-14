from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from .models import *
from api.models import IconsClass

class ProjectViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.category = ProjectCategory.objects.create(category_name="Web Development")
        self.tech1 = IconsClass.objects.create(name="Django", class_name="django-icon")
        self.tech2 = IconsClass.objects.create(name="React", class_name="react-icon")


        image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        self.project = Project.objects.create(
            title="Test Project",
            description="A test project.\nWith multiple lines.",
            image=image_file,
            feathered=True,
            github_url="https://github.com/test/test",
            demo_url="https://demo.test",
            documents_url="https://docs.test",
        )

        self.project_detail = ProjectDetail.objects.create(
            full_description="Project description",
            start_date=timezone.now().date(),
            end_date=None,
            role="Developer",
            status="In Progress",
            client="Test Client",
            project=self.project,
        )

        self.project.category.add(self.category)
        self.project.main_technologies.add(self.tech1)
        self.project_detail.full_technologies.add(self.tech1, self.tech2)

        self.gallery = ProjectGallery.objects.create(
            alternative_text="Alt 1",
            image=image_file,
            project=self.project
        )

        self.feature = KeyFeatures.objects.create(
            name="Feature 1",
            project=self.project
        )

        self.projects = reverse('projects:projects')
        self.projects_detail = lambda pk: reverse('projects:project-detail', kwargs={'project_id': pk})

    def tearDown(self):
        self.project.image.delete(save=False)
        for img in ProjectGallery.objects.all():
            img.image.delete(save=False)

    def test_get_projects_list(self):
        response = self.client.get(self.projects)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Project")
        self.assertEqual(response.data[0]['category'], ["Web Development"])
        self.assertEqual(response.data[0]['featured'], True)

    def test_get_project_detail(self):
        pk = self.project.pk
        url = self.projects_detail(pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Project")
        self.assertEqual(response.data['project_details']['role'], "Developer")
        self.assertEqual(response.data['project_details']['key_features'], ["Feature 1"])
        self.assertEqual(response.data['project_details']['full_tech_stack'][0]['name'], "Django")

    def test_get_project_detail_not_found(self):
        response = self.client.get('/projects/999/')  # Non-existent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
