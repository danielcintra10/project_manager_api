from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "mobile_phone",
        "role",
        "is_active",
    ]
    list_filter = [
        "first_name",
        "last_name",
        "email",
    ]


admin.site.register(User, UserAdmin)
