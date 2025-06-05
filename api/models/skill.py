from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime
from .icons_class import IconsClass

class Skill(models.Model):
    """
    Model to store skill for portfolio pages
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the skill list (e.g., Programming Languages, Frameworks)"),
    )

    icon_class = models.ForeignKey(IconsClass,
                                   related_name='skills',
                                   on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        verbose_name = _("Skill List")
        verbose_name_plural = _("Skill Lists")
        ordering = ["name"]

    def __str__(self):
        return self.name