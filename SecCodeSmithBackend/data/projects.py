from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime
from icons import Icon
from project_category import ProjectCategory


class ProjectDetails(models.Model):
    """
    Model to store detailed information about a project
    """
    descriptions = models.JSONField(null=True, blank=True) 
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    client = models.CharField(max_length=100, null=True, blank=True)
    keyFeatures = models.JSONField(null=True, blank=True) 
    gallery = models.JSONField(null=True, blank=True) 
    fullTechStack = models.ManyToManyField(Icon, blank=True)

    @property
    def dateFormatted(self):
        if self.startDate and self.endDate:
            return f"{self.startDate.strftime('%b %Y')} - {self.endDate.strftime('%b %Y')}"
        elif self.startDate:
            return f"Since {self.startDate.strftime('%b %Y')}"
        return None

    def __str__(self):
        return f"Details for Project" # Consider linking to parent project if possible

class Project(models.Model):
    """
    Model to store projects for portfolio pages
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    projectDetails = models.OneToOneField(ProjectDetails, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='project_images/')
    category = models.ManyToManyField(ProjectCategory)
    featured = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Icon)
    githubLink = models.URLField(null=True, blank=True)
    demoLink = models.URLField(null=True, blank=True)
    documentationLink = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
