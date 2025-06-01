from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime
import skill

class SkillList(models.Model):
    """
    Model to store skill lists for portfolio pages
    """
    list_name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the skill list (e.g., Programming Languages, Frameworks)"),
    )
    class_name = models.CharField(
        max_length=100,
        verbose_name=_("Class Name"),
        help_text=_("CSS class name for the skill list (e.g., 'skill-list')"),
    )
    list_of_skills = models.ManyToManyField(
        skill.Skill,
        verbose_name=_("Skills"),
        help_text=_("Skills included in this list (e.g., Python, JavaScript)"),
        related_name="skill_lists",
    )

    class Meta:
        verbose_name = _("Skill List")
        verbose_name_plural = _("Skill Lists")
        ordering = ["name"]

    def __str__(self):
        return self.name