from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime
from .icons import Icons


class SocialLink(models.Model):
    """
    Model to store soclial links for portfolio pages
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the social link (e.g., GitHub, LinkedIn)"),
    )
    
    url = models.URLField(
        max_length=200,
        verbose_name=_("URL"),
        help_text=_("URL of the social link"),
    )

    icon_class = models.ManyToManyField(
        Icons,
        verbose_name=_("Icon"),
        help_text=_("Icon associated with the social link (e.g., 'fab fa-github')"),
        related_name="social_links",
    )

    footer = models.BooleanField(
        default=False,
        verbose_name=_("Footer"),
        help_text=_("Whether to display this link in the footer"),
    )

    contact_pages = models.BooleanField(
        default=False,
        verbose_name=_("Contact Pages"),
        help_text=_("Whether to display this link on contact pages"),
    )

    about_pages = models.BooleanField(
        default=False,
        verbose_name=_("About Pages"),
        help_text=_("Whether to display this link on about pages"),
    )

    class Meta:
        verbose_name = _("Social Link")
        verbose_name_plural = _("Social Links")
        ordering = ["name"]

    def __str__(self):
        return self.name    