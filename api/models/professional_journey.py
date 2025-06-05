from django.db import models
from django.utils.translation import gettext_lazy as _
from pygments.lexers import q


class ProfessionalJourney(models.Model):
    """
    Model for professional journey
    """
    title = models.CharField(_("Technical Arsenal Name"), max_length=100)
    company = models.CharField(_("Technical Arsenal Company"), max_length=100)
    duration = models.CharField(_("Technical Arsenal Duration"), max_length=100)
    description = models.TextField(_("Technical Arsenal Description"))

    def __str__(self):
        return self.title