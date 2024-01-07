from django.apps import AppConfig


class ProjectManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_manager'

    def ready(self):
        import project_manager.signals
