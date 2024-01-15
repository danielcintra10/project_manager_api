from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import date
from project_manager.views import ListCreateProject, RetrieveUpdateDestroyProject, ListCreateTask, \
    RetrieveUpdateDestroyTask, ListProjectsByProjectManager, ListTasksByDeveloper, ListDeveloperTasksInProject, \
    ListAvailableDevelopers, EnableProject, DisableProject, EnableTask, DisableTask
from project_manager.models import Project, Task

User = get_user_model()


class TestUrls(TestCase):
    """Test that views have the correct routing"""

    def setUp(self):
        self.test_dev_user = User.objects.create_user(id=1,
                                                      email='robert@gmail.com',
                                                      first_name='Robert',
                                                      last_name='Lopez',
                                                      role='D',
                                                      mobile_phone='+53 59876543',
                                                      password='1234')

        self.test_pm_user = User.objects.create_user(id=2,
                                                     email='dany@gmail.com',
                                                     first_name='Daniel',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 54876543',
                                                     password='fcb')

        self.test_project = Project.objects.create(code="test-project-012024", name="Test Project",
                                                   description="Project Description",
                                                   project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                   updated_by=self.test_pm_user)

        self.test_task = Task.objects.create(code="test-task-012024", title="Test Task", description="Task Description",
                                             developer=self.test_dev_user, project=self.test_project,
                                             is_completed=False, final_date=date(9999, 10, 10),
                                             created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)

    def test_list_create_project_url_resolve(self):
        url = reverse('list_create_project')
        self.assertEquals(resolve(url).func.view_class, ListCreateProject)

    def test_retrieve_update_destroy_project_url_resolve(self):
        url = reverse('retrieve_update_destroy_project', args=['test-project-012024'])
        self.assertEquals(resolve(url).func.view_class, RetrieveUpdateDestroyProject)

    def test_list_create_task_url_resolve(self):
        url = reverse('list_create_task')
        self.assertEquals(resolve(url).func.view_class, ListCreateTask)

    def test_retrieve_update_destroy_task_url_resolve(self):
        url = reverse('retrieve_update_destroy_task', args=['test-task-012024'])
        self.assertEquals(resolve(url).func.view_class, RetrieveUpdateDestroyTask)

    def test_list_projects_by_project_manager_url_resolve(self):
        url = reverse('list_projects_by_project_manager', args=[2])
        self.assertEquals(resolve(url).func.view_class, ListProjectsByProjectManager)

    def test_list_tasks_by_developer_url_resolve(self):
        url = reverse('list_tasks_by_developer', args=[1])
        self.assertEquals(resolve(url).func.view_class, ListTasksByDeveloper)

    def test_list_developer_tasks_in_project_url_resolve(self):
        url = reverse('list_developer_tasks_in_project', args=[1, 'test-project-012024'])
        self.assertEquals(resolve(url).func.view_class, ListDeveloperTasksInProject)

    def test_list_available_developers_url_resolve(self):
        url = reverse('list_available_developers')
        self.assertEquals(resolve(url).func.view_class, ListAvailableDevelopers)

    def test_enable_project_url_resolve(self):
        url = reverse('enable_project', args=['test-project-012024'])
        self.assertEquals(resolve(url).func.view_class, EnableProject)

    def test_disable_project_url_resolve(self):
        url = reverse('disable_project', args=['test-project-012024'])
        self.assertEquals(resolve(url).func.view_class, DisableProject)

    def test_enable_task_url_resolve(self):
        url = reverse('enable_task', args=['test-task-012024'])
        self.assertEquals(resolve(url).func.view_class, EnableTask)

    def test_disable_task_url_resolve(self):
        url = reverse('disable_task', args=['test-task-012024'])
        self.assertEquals(resolve(url).func.view_class, DisableTask)

