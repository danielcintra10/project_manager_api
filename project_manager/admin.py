from django.contrib import admin
from . models import Project, Task

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('code', )
    list_display = ['code', 'name', 'project_manager', 'is_active', ]
    list_filter = ['code', 'name', ]


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('code', )
    list_display = ['code', 'title', 'developer', 'project', 'is_completed', 'is_active', ]
    list_filter = ['code', 'title', ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
