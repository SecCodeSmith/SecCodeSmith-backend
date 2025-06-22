from django.contrib import admin
from api.models import *
# ===========================
#  Basic lookup / autocomplete helpers
# ===========================

class AutocompleteByNameMixin:
    """Enable select2-style look‑ups for large FK/M2M relations."""
    search_fields = ("name",)
    ordering = ("name",)


# ===========================
#  Icons & Languages
# ===========================

@admin.register(IconsClass)
class IconsClassAdmin(admin.ModelAdmin):
    list_display = ("name", "class_name", "description")
    search_fields = ("name", "class_name")
    ordering = ("name",)


@admin.register(Lang)
class LangAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code")
    search_fields = ("name", "iso_code")
    ordering = ("name",)


# ===========================
#  Contact & Social
# ===========================

@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "icon_class",
        "footer",
        "contact_pages",
        "about_pages",
    )
    autocomplete_fields = ("icon_class",)
    list_filter = ("footer", "contact_pages", "about_pages")
    search_fields = ("name", "url")

class CommentInline(admin.TabularInline):
    model = FAQ
    extra = 0
    fields = ("question", "answer",)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "business_email", "phone", "language")
    list_filter = ("language",)
    search_fields = ("email", "business_email", "phone")
    autocomplete_fields = ("language",)
    inlines = [CommentInline]


# ===========================
#  Skills & Skill Cards
# ===========================

class SkillInline(admin.TabularInline):
    model = SkillsCard.skills.through
    extra = 1
    verbose_name = "Skill"
    verbose_name_plural = "Skills"
    autocomplete_fields = ("skill",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_class")
    search_fields = ("name",)
    autocomplete_fields = ("icon_class",)


@admin.register(SkillsCard)
class SkillsCardAdmin(admin.ModelAdmin):
    list_display = ("category_title", "icon_class")
    search_fields = ("category_title",)
    autocomplete_fields = ("icon_class",)
    filter_horizontal = ("skills",)  # nicer UI than inline when many skills exist


# ===========================
#  Core Values & FAQ
# ===========================

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "icon")
    search_fields = ("title",)
    autocomplete_fields = ("icon",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "contact")
    search_fields = ("question", "answer")
    autocomplete_fields = ("contact",)


# ===========================
#  Professional Journey & Technical Arsenal
# ===========================

@admin.register(ProfessionalJourney)
class ProfessionalJourneyAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "start_date", "end_date", "duration")
    search_fields = ("title", "company", "description")
    list_filter = ("company", "start_date", "end_date")
    date_hierarchy = "start_date"


@admin.register(TechnicalArsenalSkill)
class TechnicalArsenalSkillAdmin(admin.ModelAdmin):
    list_display = ("text",)
    search_fields = ("text",)

class TechnicalArsenalSkillInLine(admin.TabularInline):
    model = TechnicalArsenalSkill
    extra = 0
    fields = ("text",)

@admin.register(TechnicalArsenal)
class TechnicalArsenalAdmin(admin.ModelAdmin):
    list_display = ("title", "icon")
    search_fields = ("title",)
    autocomplete_fields = ("icon",)
    inlines = [TechnicalArsenalSkillInLine]


# ===========================
#  Testimonials & About
# ===========================


class JourneyInline(admin.TabularInline):
    model = ProfessionalJourney
    extra = 0
    fields = ("title", "company", "start_date", "end_date", "description")


class TechnicalArsenalInline(admin.TabularInline):
    model = TechnicalArsenal
    extra = 0
    fields = ("icon", "title")
    autocomplete_fields = ("icon",)
    show_change_link = True
    show_full_result_link = True

class TestimonialInline(admin.TabularInline):
    model = Testimonials
    extra = 0
    fields = ("author", "email", "position", "text", )

@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ("author", "email", "position")
    search_fields = ("author", "email", "position", "text")


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("lang", "about_title")
    search_fields = ("about_title", "about_text")
    autocomplete_fields = ("lang",)
    inlines = [JourneyInline, TechnicalArsenalInline, TestimonialInline, ]

