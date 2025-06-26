import io
import os
import uuid

from PIL import Image as PILImage
from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify

from .models import (
    ProjectCategory,
    ProjectDetail,
    Project,
    ProjectGallery,
    KeyFeatures, ProjectTechnology,
)


class KeyFeaturesInline(admin.TabularInline):
    model = KeyFeatures
    extra = 1
    ordering = ['name']
    ordering = ['id', ]



class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1
    ordering = ['id']
    readonly_fields = ['image_tag']


class ProjectDetailInline(admin.StackedInline):
    model = ProjectDetail
    extra = 1
    max_num = 1
    ordering = ['-start_date']
    fields = (
        'client',
        'role',
        'start_date',
        'end_date',
        'full_description',
        'full_technologies',
        'status'
    )
    filter_horizontal = ('full_technologies',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'feathered',
        'get_categories',
        'github_url',
        'demo_url',
        'documents_url',
        'get_status',
        'image_tag',
    )
    readonly_fields = ('image_tag',)
    list_filter = (
        'feathered',
        'category',
    )
    search_fields = (
        'title',
        'description',
        'projectdetail__client',
        'projectdetail__role',
    )
    filter_horizontal = (
        'category',
        'main_technologies',
    )
    inlines = [KeyFeaturesInline, ProjectGalleryInline, ProjectDetailInline]
    list_select_related = ()
    prefetch_related = ('category', 'projectdetail_set')

    def get_queryset(self, request):
        """Optimize queries by prefetching related fields."""
        qs = super().get_queryset(request)
        return qs.prefetch_related('category', 'projectdetail_set')

    def get_categories(self, obj):
        """Display a comma-separated list of category names."""
        return ", ".join(c.category_name for c in obj.category.all())
    get_categories.short_description = 'Categories'

    def get_status(self, obj):
        """Retrieve the most recent project detail's status."""
        detail = obj.projectdetail_set.order_by('-start_date').first()
        return detail.status if detail else None
    get_status.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data and obj.image:
            old_name = None
            if change:  # obj.pk exists and we're updating
                old_obj = self.model.objects.filter(pk=obj.pk).first()
                if old_obj and old_obj.image:
                    old_name = old_obj.image.name

            # File name
            base, ext = os.path.splitext(obj.image.name)

            obj.name = obj.title or base
            slug = slugify(obj.title)
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

            if old_name and default_storage.exists(old_name):
                default_storage.delete(old_name)

            obj.image.name = new_name
        super().save_model(request, obj, form, change)


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'short')
    search_fields = ('category_name',)
    autocomplete_fields = ('icon',)
    prepopulated_fields = {'short': ('category_name',)}
    ordering = ('short', )

@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name',)
    autocomplete_fields = ('icon',)
