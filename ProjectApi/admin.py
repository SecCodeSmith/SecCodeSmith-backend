from django.contrib import admin
from .models import (
    ProjectCategory,
    ProjectDetail,
    Project,
    ProjectGallery,
    KeyFeatures,
)


class KeyFeaturesInline(admin.TabularInline):
    model = KeyFeatures
    extra = 1
    ordering = ['name']


class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1
    ordering = ['id']


class ProjectDetailInline(admin.StackedInline):
    model = ProjectDetail
    extra = 1
    ordering = ['-start_date']
    fields = (
        'client',
        'role',
        'status',
        'start_date',
        'end_date',
        'full_description',
        'full_technologies',
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
    )
    list_filter = (
        'feathered',
        'category',
        'projectdetail__status',
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
    inlines = [ProjectDetailInline, KeyFeaturesInline, ProjectGalleryInline]
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


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)
