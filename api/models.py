from django.db import models
from django.utils.translation import gettext_lazy as _

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

    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.class_name

class Lang(models.Model):
    """
    Model for language data.
    """
    name = models.CharField(_("Language Name"), max_length=100)
    iso_code = models.CharField(_("ISO Code"), max_length=3)

class Contact(models.Model):
    """
    Model for contact information in diffrent languages
    """
    email = models.EmailField()
    business_email = models.EmailField()
    phone = models.CharField(max_length=12)
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

class CoreValue(models.Model):
    """
    Model to store core values
    """
    title = models.CharField(_('title'), max_length=100)
    icon = models.ForeignKey(IconsClass,
                             on_delete=models.PROTECT,
                             verbose_name=_('icon'))
    description = models.TextField(_('description'))

    class Meta:
        verbose_name = _('core value')
        verbose_name_plural = _('core values')

    def __str__(self):
        return "Title: {} Text: {}".format(self.title, self.description)

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

class ProfessionalJourney(models.Model):
    """
    Model for professional journey
    """
    title = models.CharField(_("Technical Arsenal Name"), max_length=100)
    company = models.CharField(_("Technical Arsenal Company"), max_length=100)
    duration = models.CharField(_("Technical Arsenal Duration"), max_length=100)
    description = models.TextField(_("Technical Arsenal Description"))

    class Meta:
        verbose_name = _('Professional Journey')

    def __str__(self):
        return self.title

class TechnicalArsenalSkill(models.Model):
    text = models.TextField(_('Technical Arsenal Skill'))
    class Meta:
        verbose_name = _('Technical Arsenal Skill')

    def __str__(self):
        return self.text

class TechnicalArsenal(models.Model):
    """"
    Model for Technical Arsenal
    """
    icon = models.ForeignKey(IconsClass, on_delete=models.CASCADE)
    title = models.CharField(_("Technical Arsenal Title"), max_length=100)
    skills = models.ManyToManyField(TechnicalArsenalSkill, verbose_name=_("Skills"), blank=True)

class Testimonials(models.Model):
    """
    Model for Testimonials
    """
    author = models.CharField(_("Author"), max_length=100)
    email = models.EmailField(_("Email"), max_length=100)
    position = models.CharField(_("Position"), max_length=100)
    text = models.TextField(_("Text"))


class About(models.Model):
    """
    Model for About in diffrent languages
    """
    about_title = models.CharField(_("About Title"), max_length=100)
    about_text = models.TextField(_("About Text"))
    lang = models.ForeignKey(Lang,
                             on_delete=models.CASCADE,
                             related_name='about_lang', unique=True)
    professional_journey = models.ManyToManyField(ProfessionalJourney, related_name='about_professional_journey')
    technical_arsenal = models.ManyToManyField(TechnicalArsenal, related_name='about_technical_arsenal')
    core_value = models.ManyToManyField(CoreValue, related_name='about_core_value')
    testimonials = models.ManyToManyField(Testimonials, related_name='about_testimonials')

    class Meta:
        verbose_name = _('About')

