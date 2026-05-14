import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise ValidationError(
                _("Parolda kamida 1 ta harf va 1 ta raqam bo'lishi kerak."),
                code='password_missing_requirements',
            )

    def get_help_text(self):
        return _("Parolda kamida 1 ta harf va 1 ta raqam bo'lishi kerak.")
