from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from simple_history.models import HistoricalRecords
from .validators import validate_name, validate_mobile_phone
from .utils import user_roles

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("Super user must be assigned to is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError(
                "Super user must be assigned to is_super_user=True."
            )
        return self.create_user(email, password, **extra_fields)

    def create(self, email=None, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=50,
        validators=[
            validate_name,
        ],
        verbose_name="Name",
    )
    last_name = models.CharField(
        max_length=50,
        validators=[
            validate_name,
        ],
        verbose_name="Last Name",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    mobile_phone = models.CharField(
        unique=True,
        validators=[
            validate_mobile_phone,
        ],
        verbose_name="Mobile Phone",
    )
    role = models.CharField(
        max_length=1, choices=user_roles, default="D", verbose_name="Role"
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    deleted = models.BooleanField(
        default=False,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "mobile_phone",
        "role",
    ]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.first_name

    def is_project_manager(self):
        return self.role == "P"
