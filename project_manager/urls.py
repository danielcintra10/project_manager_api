from django.urls import path
from .views import (
    ListCreateProject,
    RetrieveUpdateDestroyProject,
    ListCreateTask,
    RetrieveUpdateDestroyTask,
    ListProjectsByProjectManager,
    ListTasksByDeveloper,
    ListDeveloperTasksInProject,
    ListAvailableDevelopers,
    EnableProject,
    DisableProject,
    EnableTask,
    DisableTask,
)

urlpatterns = [
    # Projects urls.
    path("projects/", ListCreateProject.as_view(), name="list_create_project"),
    path(
        "projects/<slug:code>/",
        RetrieveUpdateDestroyProject.as_view(),
        name="retrieve_update_destroy_project",
    ),
    path(
        "projects/<slug:code>/enable",
        EnableProject.as_view(),
        name="enable_project",
    ),
    path(
        "projects/<slug:code>/disable",
        DisableProject.as_view(),
        name="disable_project",
    ),
    path(
        "projects/<int:project_manager_id>",
        ListProjectsByProjectManager.as_view(),
        name="list_projects_by_project_manager",
    ),
    # Tasks urls.
    path("tasks/", ListCreateTask.as_view(), name="list_create_task"),
    path(
        "tasks/<slug:code>/",
        RetrieveUpdateDestroyTask.as_view(),
        name="retrieve_update_destroy_task",
    ),
    path("tasks/<slug:code>/enable", EnableTask.as_view(), name="enable_task"),
    path(
        "tasks/<slug:code>/disable", DisableTask.as_view(), name="disable_task"
    ),
    path(
        "tasks/<int:developer_id>",
        ListTasksByDeveloper.as_view(),
        name="list_tasks_by_developer",
    ),
    path(
        "tasks/<int:developer_id>/<slug:project_code>",
        ListDeveloperTasksInProject.as_view(),
        name="list_developer_tasks_in_project",
    ),
    # Extra urls.
    path(
        "available-developers/",
        ListAvailableDevelopers.as_view(),
        name="list_available_developers",
    ),
]
