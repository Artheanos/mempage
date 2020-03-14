from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_domain_only_email(value):
    """
    Let's validate the email passed is in the domain "yourdomain.com"
    """
    if "yourdomain.com" not in value:
        raise ValidationError(
            _("Sorry, the email submitted is invalid. All emails have to be registered on this domain only."),
            status='invalid')
