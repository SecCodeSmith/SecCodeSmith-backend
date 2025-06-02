from django.db import models
from django.utils.translation import gettext_lazy as _

class Icons(models.Model):
    """
    Model to store icons for portfolio pages
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the icon (e.g., GitHub, LinkedIn)"),
    )
    class_name = models.CharField(
        max_length=100,
        verbose_name=_("Class Name"),
        help_text=_("CSS class name for the icon (e.g., 'fab fa-github')"),
    )

    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")
        ordering = ["name"]

    def __str__(self):
        return self.name