from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime
from .icons import Icons

class Testimonial(models.Model):
    """
    Model to store testimonials for portfolio pages
    """
    author = models.CharField(
        max_length=100,
        verbose_name=_("Author"),
        help_text=_("Name of the person giving the testimonial"),
    )
    
    content = models.TextField(
        verbose_name=_("Content"),
        help_text=_("Content of the testimonial"),
    )
    
    date = models.DateField(
        default=date.today,
        verbose_name=_("Date"),
        help_text=_("Date when the testimonial was given"),
    )
    
    icon_class = models.ForeignKey(
        Icons,
        on_delete=models.CASCADE,
        verbose_name=_("Icon"),
        help_text=_("Icon associated with the testimonial (e.g., 'fas fa-quote-left')"),
        related_name="testimonials",
    )

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.author} - {self.date}"