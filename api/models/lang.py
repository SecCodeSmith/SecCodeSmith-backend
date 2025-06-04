from django.db import models
from django.utils.translation import gettext_lazy as _

class Lang(models.Model):
    """
    Model for language data.
    """
    name = models.CharField(_("Language Name"), max_length=100)
    iso_code = models.CharField(_("ISO Code"), max_length=3)