from django.db import models
from django.db.models.fields.related import RelatedField
from django.utils.translation import gettext_lazy as _
from .icons_class import IconsClass
from .skill import Skill

class SkillsCard(models.Model):
    """
    List of skills cards
    """
    category_title = models.CharField(
        max_length=100,
        verbose_name=_("Category title"),
        help_text=_("Name of skills card")
    )

    icon_class = models.ForeignKey(IconsClass,
                                   related_name='skills_cards',
                                   on_delete=models.SET_NULL,
                                   null=True)
    skills = models.ManyToManyField(Skill,)