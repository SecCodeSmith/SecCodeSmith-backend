from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from api.models import IconsClass

class ProjectCategory(models.Model):
    """
    Model for project categories
    """
    category_name = models.CharField(max_length=200)
    short = models.CharField(max_length=10, unique=True)

class Project(models.Model):
    """
    Model for project data.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='project/')
    category = models.ManyToManyField(ProjectCategory)
    feathered = models.BooleanField(default=False)
    main_technologies = models.ManyToManyField(IconsClass, related_name='main_technologies')
    github_url = models.URLField(null=True, blank=True)
    demo_url = models.URLField(null=True, blank=True)
    documents_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    @admin.display
    def image_tag(self):
        return format_html('<img src="{}" height="100" />',
                           self.image.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class ProjectDetail(models.Model):
    """
    Model for project details.
    """
    full_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    full_technologies = models.ManyToManyField(IconsClass, related_name='full_technologies')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

class ProjectGallery(models.Model):
    """
    Model for project gallery
    """
    alternative_text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='project_gallery/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @admin.display
    def image_tag(self):
        return format_html('<img src="{}" height="100" />',
                           self.image.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class KeyFeatures(models.Model):
    """
    Model for key features
    """
    name = models.CharField(max_length=200)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)