import io
import os
import uuid

from PIL import Image as PILImage
from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.html import format_html
from django.utils.text import slugify

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image_tag","image", "name", "alt")
    search_fields = ("name", "alt")
    readonly_fields = ("image_tag",)

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data and obj.image:

            old_name = None
            if change:  # obj.pk exists and we're updating
                old_obj = self.model.objects.filter(pk=obj.pk).first()
                if old_obj and old_obj.image:
                    old_name = old_obj.image.name

            # File name
            base, ext = os.path.splitext(obj.image.name)

            obj.name = obj.name or base
            slug = slugify(obj.name)
            new_name = f"{slug}-{uuid.uuid4().hex}.webp"

            if ext != '.webp':
                img = PILImage.open(obj.image)
                img = img.convert('RGBA')
                buff = io.BytesIO()
                img.save(buff, format='WEBP', quality=85, method=6)
                buff.seek(0)
                obj.image.save(new_name, ContentFile(buff.read()), save=False)
                img.close()
            else:
                obj.image.storage.save(new_name, obj.image.file)
                obj.image.name = new_name

            if old_name and default_storage.exists(old_name):
                default_storage.delete(old_name)

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete(save=False)
        super().delete_model(request, obj)
