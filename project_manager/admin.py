from django.contrib import admin
from .models import Project, Task, EmailLog

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ("code",)
    list_display = [
        "code",
        "name",
        "project_manager",
        "is_active",
    ]
    list_filter = [
        "code",
        "name",
    ]


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("code",)
    list_display = [
        "code",
        "title",
        "developer",
        "project",
        "is_completed",
        "is_active",
    ]
    list_filter = [
        "code",
        "title",
    ]


class EmailLogAdmin(admin.ModelAdmin):
    readonly_fields = (
        "destination_email",
        "email_purpose",
        "task",
        "delivered",
        "error_info",
        "created_at",
    )
    list_display = [
        "destination_email",
        "email_purpose",
        "task",
        "delivered",
        "error_info",
        "created_at",
    ]
    list_filter = [
        "destination_email",
        "email_purpose",
        "delivered",
        "task",
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(EmailLog, EmailLogAdmin)
