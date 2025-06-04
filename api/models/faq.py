from django.db import models
from django.utils.translation import gettext_lazy as _
from .contact import Contact
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