from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime

class ProjectCategory(models.Model):
    """
    Model to store project categories for portfolio pages
    """
    fullName = models.CharField(max_length=100)
    shortName = models.CharField(max_length=50)
    icon = models.CharField(max_length=100)  # Or models.ImageField/FileField if storing icons

    def __str__(self):
        return self.fullName