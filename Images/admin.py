from django.contrib import admin
from django.utils.html import format_html
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "name", "alt")
    search_fields = ("name", "alt")
    readonly_fields = ("thumbnail",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;border-radius:4px;" alt="{}">',
                obj.image.url,
                obj.alt or "",
            )
        return "—"

    thumbnail.short_description = "Preview"
