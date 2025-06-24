from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.core.validators import URLValidator
from api.validator import *

class IconsClass(models.Model):
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
        help_text=_("CSS class categorry_title for the icon (e.g., 'fab fa-github')"),
    )

    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SocialLinks(models.Model):
    """
    Model to store soclial links for portfolio pages
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the social link (e.g., GitHub, LinkedIn)"),
    )

    url = models.CharField(
        max_length=200,
        verbose_name=_("URL"),
        help_text=_("URL of the social link"),
        validators=[validate_url_or_mailto,]
    )

    icon_class = models.ForeignKey(
        IconsClass,
        on_delete=models.SET_NULL,
        null=True,
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


class Lang(models.Model):
    """
    Model for language data.
    """
    name = models.CharField(_("Language Name"), max_length=100)
    iso_code = models.CharField(_("ISO Code"), max_length=3)

    def __str__(self):
        return self.name

class Contact(models.Model):
    """
    Model for contact information in diffrent languages
    """
    email = models.EmailField(null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    map_iframe = models.URLField()
    language = models.ForeignKey(Lang,
                                 on_delete=models.CASCADE,
                                 related_name='contact_lang', )

    def __str__(self):
        return ('Email: {} Business email {} Phone {} Lang {}'
                .format(self.email, self.business_email, self.phone, self.language))

class Skill(models.Model):
    """
    Model to store skill for portfolio pages
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the skill list (e.g., Programming Languages, Frameworks)"),
    )

    icon_class = models.ForeignKey(IconsClass,
                                   related_name='skills',
                                   on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        verbose_name = _("Skill List")
        verbose_name_plural = _("Skill Lists")
        ordering = ["name"]

    def __str__(self):
        return self.name

class SkillsCard(models.Model):
    """
    List of skills cards
    """
    category_title = models.CharField(
        max_length=100,
        verbose_name=_("Category title"),
        help_text=_("Name of skills card")
    )

    icon_class = models.ForeignKey(IconsClass,
                                   related_name='skills_cards',
                                   on_delete=models.SET_NULL,
                                   null=True)
    skills = models.ManyToManyField(Skill,)

    def __str__(self):
        return self.category_title



class FAQ(models.Model):
    """
    Model for FAQ
    """
    question = models.CharField(_('Question'), max_length=200)
    answer = models.TextField(_('Answer'))
    contact = models.ForeignKey(Contact,
                                on_delete=models.CASCADE,
                                verbose_name=_('Contact'),)
    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

    def __str__(self):
        return self.question



class About(models.Model):
    """
    Model for About in diffrent languages
    """
    about_title = models.CharField(_("About Title"), max_length=100)
    sub_title = models.CharField(_("Sub Title"), max_length=100)
    about_text = models.TextField(_("About Text"))
    image_title = models.CharField(_("Image Title"),
                                   max_length=100,
                                   default="The Master Behind the Mask")
    image = models.ImageField(_("About Image"),)
    lang = models.OneToOneField(Lang,
                             on_delete=models.CASCADE,
                             related_name='about_lang')
    technical_arsenal_title = models.CharField(_("Technical Arsenal Title"),
                                               max_length=100, default="Arsenal of Expertise")
    core_value_title = models.CharField(_("Core Value Title"), max_length=100,
                                        default="Forging Principles")
    professional_journal_title = models.CharField(_("Professional Journal Title"), max_length=100,
                                                  default="The Smith's Journey")
    testimonials_title = models.CharField(_("Testimonials Title"), max_length=100,
                                          default="Testimonials")


    class Meta:
        verbose_name = _('About')

    def __str__(self):
        return self.about_title

    @admin.display
    def image_tag(self):
        return format_html('<img src="{}" alt={} height="100" />',
                           self.image.url, self.about_title)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class ProfessionalJourney(models.Model):
    """
    Model for professional journey
    """
    title = models.CharField(_("Job title"), max_length=100)
    company = models.CharField(_("Company name"), max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    about = models.ForeignKey(About, on_delete=models.CASCADE,
                              verbose_name=_('About_ProfessionalJourney'), null=True)

    @property
    def duration(self):
        """
        Compute duration between start_date and end_date in years/months.
        """
        start_date = self.start_date.strftime('%m.%Y')
        end_date = self.end_date.strftime('%m.%Y') if self.end_date else 'Now'

        return '{}-{}'.format(start_date, end_date)


    class Meta:
        verbose_name = _('Professional Journey')


    def __str__(self):
        return self.title

class TechnicalArsenal(models.Model):
    """"
    Model for Technical Arsenal
    """
    icon = models.ForeignKey(IconsClass, on_delete=models.CASCADE)
    title = models.CharField(_("Technical Arsenal Title"), max_length=100)
    about = models.ForeignKey(About, on_delete=models.CASCADE,
                              verbose_name=_('Technical Arsenal Skill'))

    def __str__(self):
        return self.title

class TechnicalArsenalSkill(models.Model):
    text = models.CharField(_('Technical Arsenal Skill'), max_length=100)
    technical_arsenal = models.ForeignKey(TechnicalArsenal, on_delete=models.CASCADE,
                              verbose_name=_('Technical Arsenal Skill'))
    class Meta:
        verbose_name = _('Technical Arsenal Skill')

    def __str__(self):
        return self.text

class Testimonials(models.Model):
    """
    Model for Testimonials
    """
    author = models.CharField(_("Author"), max_length=100)
    email = models.EmailField(_("Email"), max_length=100)
    position = models.CharField(_("Position"), max_length=100)
    text = models.TextField(_("Text"))
    about = models.ForeignKey(About, on_delete=models.CASCADE,
                              verbose_name=_('Technical Arsenal Skill'))

class CoreValue(models.Model):
    """
    Model to store core values
    """
    title = models.CharField(_('title'), max_length=100)
    icon = models.ForeignKey(IconsClass,
                             on_delete=models.CASCADE,
                             verbose_name=_('icon'))
    description = models.TextField(_('description'))

    about = models.ForeignKey(About, on_delete=models.CASCADE,
                              verbose_name=_('Core value about'))

    class Meta:
        verbose_name = _('core value')
        verbose_name_plural = _('core values')

    def __str__(self):
        return "Title: {} Text: {}".format(self.title, self.description)
