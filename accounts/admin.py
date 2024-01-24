from django.contrib import admin
from django.contrib.auth import get_user_model
from secrets import compare_digest

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

    def save_model(self, request, obj, form, change):
        # Verify if user already exist in the database
        if obj.pk:
            user = User.objects.filter(pk=obj.pk).first()
            if not compare_digest(user.password, obj.password):
                obj.set_password(obj.password)
        else:
            # For new users always encrypt password
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
