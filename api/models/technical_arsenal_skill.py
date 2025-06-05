from django.db import models
from django.utils.translation import gettext_lazy as _
from .technical_arsenal import TechnicalArsenal

class TechnicalArsenalSkill(models.Model):
    text = models.TextField(_('Technical Arsenal Skill'))
    technical_arsenal = models.ForeignKey(TechnicalArsenal, on_delete=models.CASCADE)
    def __str__(self):
        return self.text
