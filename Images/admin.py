from django.contrib import admin
from django.utils.html import format_html
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image_tag","image", "name", "alt")
    search_fields = ("name", "alt")
    readonly_fields = ("image_tag",)

