import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
'''
This file/class is just using regex so the user is bound to provide complex passwords
'''
class CustomPasswordValidator:
    def validate(self, password, user=None):
        print(password)
        print("dajsvhgwdsv")
        # Minimum 8 characters
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'), code='password_too_short')

        # Must contain at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'), code='password_no_upper')

        # Must contain at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'), code='password_no_lower')

        # Must contain at least one digit
        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one digit.'), code='password_no_digit')

        # Must contain at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_('Password must contain at least one special character.'), code='password_no_special')

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long, contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character."
        )

    
