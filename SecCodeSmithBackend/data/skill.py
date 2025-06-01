from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime

class SkillList(models.Model):
    """
    Model to store skill lists for portfolio pages
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the skill list (e.g., Programming Languages, Frameworks)"),
    )

    class_name = models.CharField(
        max_length=100,
        verbose_name=_("Class Name"),
        help_text=_("CSS class name for the skill list (e.g., 'skill-list')"),
    )

    class Meta:
        verbose_name = _("Skill List")
        verbose_name_plural = _("Skill Lists")
        ordering = ["name"]

    def __str__(self):
        return self.name