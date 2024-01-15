from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('project-manager/', include('project_manager.urls')),
]
