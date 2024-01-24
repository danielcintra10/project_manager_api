from django.core.exceptions import ValidationError
import re


def validate_name(name):
    if re.findall(r"[^a-z-A-Z ÁÉÍÓÚáéíóúÑñ]", name):
        raise ValidationError(f"{name}, Names can only contain letters ")


def validate_mobile_phone(mobile_phone):
    if re.findall(r"[^0-9 +]", mobile_phone):
        raise ValidationError(
            f"{mobile_phone}, mobile phone can only contain numbers and the special character +"
        )
