from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from .models import *
from api.models import IconsClass

class ProjectModelsTest(TestCase):
    def setUp(self):
        self.category = ProjectCategory.objects.create(category_name="Web Development")
        self.tech1 = IconsClass.objects.create(name="Django", class_name="django-icon")
        self.tech2 = IconsClass.objects.create(name="React", class_name="react-icon")
        image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project.",
            image=image_file,
            feathered=True,
            github_url="https://github.com/test/test",
            demo_url="https://demo.test",
            documents_url="https://docs.test",
            start_date=timezone.now().date(),
            end_date=None,
            role="Developer",
            status="In Progress",
            client="Test Client",
        )

        self.project.category.add(self.category)
        self.project.main_technologies.add(self.tech1)
        self.project.full_technologies.add(self.tech1, self.tech2)
        self.gallery1 = ProjectGallery.objects.create(
            alternative_text="Alt 1",
            image=image_file,
            project=self.project,
        )
        self.feature = KeyFeatures.objects.create(
            name="Feature 1",
            project=self.project,
        )

    def tearDown(self):
        self.project.image.delete(save=False)
        for img in ProjectGallery.objects.all():
            img.image.delete(save=False)

    def test_category_str(self):
        self.assertEqual(str(self.category.category_name), "Web Development")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_relationships(self):
        self.assertEqual(self.project.category.first(), self.category)
        self.assertIn(self.tech1, self.project.main_technologies.all())
        self.assertIn(self.tech2, self.project.full_technologies.all())

    def test_gallery_and_feature_creation(self):
        self.assertEqual(self.project.projectgallery_set.count(), 1)
        self.assertEqual(self.project.keyfeatures_set.count(), 1)
        self.assertEqual(self.gallery1.project, self.project)
        self.assertEqual(self.feature.project, self.project)

    def test_cascade_delete(self):
        project_id = self.project.id
        self.project.delete()
        self.assertFalse(Project.objects.filter(id=project_id).exists())
        self.assertFalse(ProjectGallery.objects.filter(project_id=project_id).exists())
        self.assertFalse(KeyFeatures.objects.filter(project_id=project_id).exists())
