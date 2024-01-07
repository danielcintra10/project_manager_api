from django.core.exceptions import ValidationError
from accounts.models import User


def validate_user_is_project_manager(user_id):
    user = User.objects.filter(id=user_id).first()
    if user.is_project_manager() is not True:
        raise ValidationError(f"{user.first_name}, is not a project manager, to lead a project "
                              f"you need a project manager")


def validate_user_is_developer(user_id):
    user = User.objects.filter(id=user_id).first()
    if user.is_project_manager():
        raise ValidationError(f"{user.first_name}, is not a developer, to assign tasks you need a developer")
