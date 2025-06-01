from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime

class ProfessionalJourney(models.Model):
    """
    Model to store professional journey details for portfolio pages
    """
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
        help_text=_("Title of the professional journey (e.g., Software Engineer at XYZ Corp)"),
    )
    
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description of the professional journey"),
    )
    
    start_date = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_("Start date of the professional journey"),
    )
    
    end_date = models.DateField(
        verbose_name=_("End Date"),
        help_text=_("End date of the professional journey (leave blank if current)"),
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = _("Professional Journey")
        verbose_name_plural = _("Professional Journeys")
        ordering = ["start_date"]
    
    def __str__(self):
        return self.title
    def is_current(self):
        """
        Check if the professional journey is currently ongoing.
        """
        return self.end_date is None or self.end_date > date.today()
    def duration(self):
        """
        Calculate the duration of the professional journey.
        Returns:
            str: Duration in years and months.
        """
        if self.end_date:
            duration = self.end_date - self.start_date
        else:
            duration = date.today() - self.start_date
        
        years = duration.days // 365
        months = (duration.days % 365) // 30
        
        return f"{years} years, {months} months" if years > 0 else f"{months} months"