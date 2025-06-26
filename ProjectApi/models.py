from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify

from api.models import IconsClass

class ProjectCategory(models.Model):
    """
    Model for project categories
    """
    category_name = models.CharField(max_length=200, unique=True)
    icon = models.ForeignKey(IconsClass, on_delete=models.SET_NULL,
                             null=True, blank=True)
    short = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.short:
            self.short = slugify(self.category_name)
        super().save(*args, **kwargs)

class ProjectTechnology(models.Model):
    icon = models.ForeignKey(IconsClass, on_delete=models.SET_NULL,
                             null=True, blank=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Model for project data.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='project/')
    category = models.ManyToManyField(ProjectCategory)
    feathered = models.BooleanField(default=False)
    main_technologies = models.ManyToManyField(ProjectTechnology,
                                               related_name='main_technologies')
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
    status = models.CharField(max_length=100, default='Active')
    end_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    client = models.CharField(max_length=100, default='Internal Project')
    full_technologies = models.ManyToManyField(ProjectTechnology,
                                               related_name='full_technologies', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name