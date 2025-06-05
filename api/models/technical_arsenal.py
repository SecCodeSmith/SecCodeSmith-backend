from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Skill
from .icons_class import IconsClass

class TechnicalArsenal(models.Model):
    """"
    Model for Technical Arsenal
    """
    icon = models.ForeignKey(IconsClass, on_delete=models.CASCADE)
    title = models.CharField(_("Technical Arsenal Title"), max_length=100)
    skills = models.ManyToManyField(Skill, verbose_name=_("Skills"), blank=True)