from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator


def validate_url_or_mailto(value):
    """
    Accepts either:
     - http:// or https:// …  (via URLValidator)
     - mailto:user@example.com  (via EmailValidator on the part after "mailto:")
    """
    if value.startswith("mailto:"):
        email = value[7:]
        try:
            EmailValidator()(email)
        except ValidationError:
            raise ValidationError("Enter a valid mailto: link, e.g. mailto:you@example.com")
    else:
        # only allow http(s) here
        URLValidator(schemes=["http", "https"])(value)