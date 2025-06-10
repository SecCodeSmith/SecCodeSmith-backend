import os

from django.contrib import admin
from django.db import models
from django.utils.text import slugify
from django.utils.html import escape, format_html


def image_upload_path(instance: "Image", filename: str) -> str:
    """
    Store every image under
        media/Images/<slugified guild name>/<original filename>
    """
    guild_slug = slugify(instance.name or "unknown")
    return os.path.join("Images", f"{guild_slug}{filename}")


class Image(models.Model):
    name = models.CharField("Guild name", max_length=50)
    image = models.ImageField(upload_to=image_upload_path)
    alt = models.CharField("Alternative text", max_length=120, blank=True, null=True)

    class Meta:
        ordering = ["alt", "name"]

    def __str__(self) -> str:   # what shows in admin list, shell, etc.
        return self.alt or self.name or f"Image {self.pk}"

    @admin.display
    def image_tag(self):
        return format_html('<img src="{}" alt={} height="100" />',
                           self.image.url, self.alt)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
