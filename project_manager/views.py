from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    DestroyAPIView, ListAPIView, UpdateAPIView
from api.serializers import ProjectSerializer, TaskSerializer, UserSerializer
from .models import Project, Task
from accounts.permissions import IsProjectManager
from .permissions import IsTaskDeveloper, IsRequestedDeveloper

User = get_user_model()


class ListCreateProject(ListCreateAPIView):
    queryset = Project.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == "POST":
            self.permission_classes = [permissions.IsAdminUser | IsProjectManager]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            context['request'] = self.request
        return context


class RetrieveUpdateDestroyProject(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectSerializer
    lookup_field = 'code'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ['DELETE', 'PUT', 'PATCH']:
            self.permission_classes = [permissions.IsAdminUser | IsProjectManager]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.is_active = False
        project.save()
        return Response({'Response': 'Project was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class ListCreateTask(ListCreateAPIView):
    queryset = Task.objects.filter(is_active=True, is_deleted=False)
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser | IsProjectManager]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            context['request'] = self.request
        context['fields'] = True
        return context


class RetrieveUpdateDestroyTask(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.filter(is_active=True, is_deleted=False)
    serializer_class = TaskSerializer
    lookup_field = 'code'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [permissions.IsAdminUser | IsProjectManager | IsTaskDeveloper]
        elif self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser | IsProjectManager]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            context['request'] = self.request
        context['fields'] = True
        return context

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.is_active = False
        task.save()
        return Response({'Response': 'Task was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class ListProjectsByProjectManager(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser | IsProjectManager]

    def get_queryset(self):
        project_manager_id = int(self.kwargs['project_manager_id'])
        queryset = Project.objects.filter(is_active=True, is_deleted=False,
                                          project_manager__id__exact=project_manager_id)
        return queryset


class ListTasksByDeveloper(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser | IsProjectManager | IsRequestedDeveloper]

    def get_queryset(self):
        developer_id = int(self.kwargs['developer_id'])
        queryset = Task.objects.filter(is_active=True, is_deleted=False,
                                       developer__id__exact=developer_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['fields'] = True
        return context


class ListDeveloperTasksInProject(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser | IsProjectManager | IsRequestedDeveloper]

    def get_queryset(self):
        developer_id = int(self.kwargs['developer_id'])
        project_code = self.kwargs['project_code']
        queryset = Task.objects.filter(is_active=True, is_deleted=False,
                                       developer__id__exact=developer_id,
                                       project__code__exact=project_code)
        if not queryset.exists():
            raise Http404("No tasks found for the given developer_id and project_code")
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['fields'] = True
        return context


class ListAvailableDevelopers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(tasks__isnull=True, role__exact='D', is_active=True, deleted=False)
    permission_classes = [permissions.IsAdminUser | IsProjectManager]


class EnableProject(UpdateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(is_active=False, is_deleted=False)
    permission_classes = [permissions.IsAdminUser | IsProjectManager]
    lookup_field = 'code'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_active = True
        project.save()
        return Response({'Response': 'Project was successfully added'}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("Partial updates are not allowed")


class DisableProject(DestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(is_active=True, is_deleted=False)
    permission_classes = [permissions.IsAdminUser | IsProjectManager]
    lookup_field = 'code'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_active = False
        project.save()
        return Response({'Response': 'Project was successfully disabled'}, status=status.HTTP_204_NO_CONTENT)


class EnableTask(UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=False, is_deleted=False)
    permission_classes = [permissions.IsAdminUser | IsProjectManager]
    lookup_field = 'code'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_active = True
        task.save()
        return Response({'Response': 'Task was successfully added'}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("Partial updates are not allowed")


class DisableTask(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(is_active=True, is_deleted=False)
    permission_classes = [permissions.IsAdminUser | IsProjectManager]
    lookup_field = 'code'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_active = False
        task.save()
        return Response({'Response': 'Task was successfully disabled'}, status=status.HTTP_204_NO_CONTENT)
