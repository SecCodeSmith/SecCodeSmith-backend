from django.db import models
from django.utils.translation import gettext_lazy as _
from .icons_class import IconsClass

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