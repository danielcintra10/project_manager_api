from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'mobile_phone', 'role', 'is_active', ]
    list_filter = ['first_name', 'last_name', 'email', ]


admin.site.register(User, UserAdmin)
