from django.db import models
from django.utils.translation import gettext_lazy as _
from .lang import Lang

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