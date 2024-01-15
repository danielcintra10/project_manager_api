from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from project_manager.models import Project, Task

User = get_user_model()


class TestBaseClass(APITestCase):
    """Base class to test project_manager endpoints"""

    def setUp(self):
        self.test_dev_user = User.objects.create_user(id=1,
                                                      email='robert@gmail.com',
                                                      first_name='Robert',
                                                      last_name='Lopez',
                                                      role='D',
                                                      mobile_phone='+53 59876543',
                                                      password='SecurePass78*01')

        self.test_dev_user_2 = User.objects.create_user(id=2,
                                                        email='karlab@gmail.com',
                                                        first_name='Karla',
                                                        last_name='Barrera',
                                                        role='D',
                                                        mobile_phone='+1 770554443',
                                                        password='Securepass001')

        self.test_dev_user_3 = User.objects.create_user(id=3,
                                                        email='heidyklaus@gmail.com',
                                                        first_name='Heidy',
                                                        last_name='Klaus',
                                                        role='D',
                                                        mobile_phone='+88 46000043',
                                                        password='Securepass#10')

        self.test_pm_user = User.objects.create_user(id=4,
                                                     email='dany@gmail.com',
                                                     first_name='Daniel',
                                                     last_name='Owens',
                                                     role='P',
                                                     mobile_phone='+31 59997777',
                                                     password='SecurepassFinal8564')

        self.test_pm_user_2 = User.objects.create_user(id=5,
                                                       email='pmusermail@gmail.com',
                                                       first_name='Jenni',
                                                       last_name='Doe',
                                                       role='P',
                                                       mobile_phone='+34 879888100',
                                                       password='password*strong23')

        self.test_project = Project.objects.create(code="test-project-01-2024", name="Test Project",
                                                   description="Project Description",
                                                   project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                   updated_by=self.test_pm_user)

        self.test_task = Task.objects.create(code="test-task-01-2024", title="Test Task",
                                             description="Task Description",
                                             developer=self.test_dev_user, project=self.test_project,
                                             is_completed=False, final_date=date(9999, 10, 10),
                                             created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)

        self.test_task_2 = Task.objects.create(code="test-task-02-2024", title="Test Task number 2",
                                               description="Task Description for task 2",
                                               developer=self.test_dev_user, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user)

        self.test_task_3 = Task.objects.create(code="test-task-03-2024", title="Test Task number 3",
                                               description="Task Description for task 3",
                                               developer=self.test_dev_user_2, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user_2,
                                               updated_by=self.test_pm_user_2)

        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')


class TestListCreateProject(TestBaseClass):
    """Test /api/v1/project-manager/projects/ endpoint"""

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/projects/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/project-manager/projects/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_dont_returns_list_of_active_and_non_deleted_projects(self):
        new_project = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                             description="Project Description for project 2",
                                             project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user, is_active=False)
        new_project_2 = Project.objects.create(code="test-project-03-2024", name="Test Project 3",
                                               description="Project Description for project 3",
                                               project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user, is_deleted=True)
        response = self.client.get('/api/v1/project-manager/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_post_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_post_request_dev_user_authenticated_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 403)

    def test_post_request_with_valid_data_creates_new_project(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 2)

    def test_post_request_with_valid_data_creates_new_project_and_set_code_auto(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        project = Project.objects.filter(code=response.data['code']).first()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(project.code is not None)

    def test_post_request_with_valid_data_sets_created_by_and_updated_by_fields_to_current_user(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 201)
        project = Project.objects.filter(code=response.data['code']).first()
        self.assertEqual(project.created_by, self.test_pm_user)
        self.assertEqual(project.updated_by, self.test_pm_user)

    def test_post_request_return_correct_data(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 201)
        project = Project.objects.filter(code=response.data['code']).first()
        self.assertEqual(response.data["code"], project.code)
        self.assertEqual(response.data["name"], project.name)
        self.assertEqual(response.data["description"], project.description)
        self.assertEqual(response.data["project_manager"], project.project_manager.id)
        self.assertEqual(response.data["tasks"], list(project.tasks.all()))

    def test_post_request_with_extra_fields_return_correct_data(self):
        data = {
            'code': 'code-487878',
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 4,
            'created_by': 2
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 201)
        project = Project.objects.filter(code=response.data['code']).first()
        self.assertEqual(response.data["code"], project.code)
        self.assertNotEqual('code-487878', project.code)
        self.assertEqual(response.data["name"], project.name)
        self.assertEqual(response.data["description"], project.description)
        self.assertEqual(response.data["project_manager"], project.project_manager.id)
        self.assertEqual(response.data["tasks"], list(project.tasks.all()))
        self.assertEqual(self.test_pm_user, project.created_by)

    def test_post_request_validate_project_manager_constraint(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 1
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_invalid_project_manager_return_400(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test endpoints",
            'project_manager': 100
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_invalid_data_return_400(self):
        data = {
            'field': "New Project Created",
            'wrong field': "Project created to test endpoints",
            'project_manager': 4
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_invalid_data_types_returns_400(self):
        data = {
            'field': 2,
            'wrong field': True,
            'project_manager': "2"
        }
        response = self.client.post('/api/v1/project-manager/projects/', data=data)
        self.assertEqual(response.status_code, 400)


class TestRetrieveUpdateDestroyProject(TestBaseClass):
    """Test /api/v1/project-manager/project/code/ endpoint, responses, permissions and constraints"""

    def test_get_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/projects/test-project-01-2024/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_with_correct_data_returns_200(self):
        response = self.client.get('/api/v1/project-manager/projects/test-project-01-2024/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_returns_correct_data(self):
        response = self.client.get('/api/v1/project-manager/projects/test-project-01-2024/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], self.test_project.code)
        self.assertEqual(response.data['name'], self.test_project.name)
        self.assertEqual(response.data['description'], self.test_project.description)
        self.assertEqual(response.data['project_manager'], self.test_project.project_manager.id)
        self.assertEqual(response.data['is_active'], self.test_project.is_active)

    def test_get_request_wrong_data_returns_404(self):
        response = self.client.get('/api/v1/project-manager/projects/000000/')
        self.assertEqual(response.status_code, 404)

    def test_put_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/')
        self.assertEqual(response.status_code, 401)

    def test_put_request_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/')
        self.assertEqual(response.status_code, 403)

    def test_put_request_correct_data_returns_200(self):
        data = {
            'name': "Project Updated",
            'description': "Project description updated for tests",
            'project_manager': 5
        }
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_request_returns_correct_data(self):
        data = {
            'name': "Project Updated",
            'description': "Project description updated for tests",
            'project_manager': 5
        }
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)
        project = Project.objects.filter(code='test-project-01-2024').first()
        self.assertEqual(self.test_project.code, project.code)
        self.assertEqual(self.test_project.is_active, project.is_active)
        self.assertEqual(self.test_project.is_deleted, project.is_deleted)
        # Updated fields
        self.assertEqual("Project Updated", project.name)
        self.assertEqual("Project description updated for tests", project.description)
        self.assertEqual(self.test_pm_user_2, project.project_manager)

    def test_put_request_auditory_fields_returns_correct_data(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'name': "Project Updated",
            'description': "Project description updated for tests",
            'project_manager': 5
        }
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)
        project = Project.objects.filter(code='test-project-01-2024').first()
        self.assertEqual(self.test_pm_user, project.created_by)
        self.assertEqual(self.test_pm_user_2, project.updated_by)

    def test_put_request_wrong_project_manager_returns_400(self):
        data = {
            'name': "Project Updated",
            'description': "Project description updated for tests",
            'project_manager': 1
        }
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_patch_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        data = {
            'name': "Project Updated",
            'description': "Project description updated for tests",
            'project_manager': 5
        }
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_patch_request_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/')
        self.assertEqual(response.status_code, 403)

    def test_patch_request_correct_data_return_200(self):
        data = {
            'name': "Project Updated",
        }
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_request_returns_correct_data(self):
        data = {
            'name': "Project Updated",
        }
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)
        project = Project.objects.filter(code='test-project-01-2024').first()
        # Updated fields
        self.assertEqual("Project Updated", project.name)
        # Non updated fields
        self.assertEqual(self.test_project.code, project.code)
        self.assertEqual(self.test_project.description, project.description)
        self.assertEqual(self.test_pm_user, project.project_manager)
        self.assertEqual(self.test_project.is_active, project.is_active)
        self.assertEqual(self.test_project.is_deleted, project.is_deleted)

    def test_patch_request_update_auditory_field_updated_by(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'name': "Project Updated",
        }
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)
        project = Project.objects.filter(code='test-project-01-2024').first()
        self.assertEqual("Project Updated", project.name)
        self.assertEqual(self.test_pm_user, project.created_by)
        self.assertEqual(self.test_pm_user_2, project.updated_by)

    def test_patch_request_wrong_project_manager_returns_400(self):
        data = {
            'name': "Project Updated",
            'project_manager': 2
        }
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_delete_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        data = {
            'name': "Project Updated",
        }
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_delete_request_authenticated_dev_user_returns_401(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'name': "Project Updated",
        }
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 403)

    def test_delete_request_returns_204(self):
        data = {
            'name': "Project Updated",
        }
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 204)

    def test_delete_request_update_fields_correctly(self):
        data = {
            'name': "Project Updated",
        }
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/', data=data)
        self.assertEqual(response.status_code, 204)
        project = Project.objects.filter(code='test-project-01-2024').first()
        self.assertEqual(False, project.is_active)
        self.assertEqual(True, project.is_deleted)


class TestListCreteTask(TestBaseClass):
    """Test /api/v1/project-manager/tasks/ endpoint, permissions, responses and constraints"""

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/tasks/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/project-manager/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_returns_correct_count_of_elements(self):
        response = self.client.get('/api/v1/project-manager/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_request_dont_returns_list_of_active_and_non_deleted_projects(self):
        new_task = Task.objects.create(code="test-task-04-2024", title="Test Task number 4",
                                       description="Task Description for task 4",
                                       developer=self.test_dev_user_2, project=self.test_project,
                                       is_completed=False, final_date=date(9999, 10, 10),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user, is_active=False, is_deleted=False)
        new_task_2 = Task.objects.create(code="test-task-05-2024", title="Test Task number 5",
                                         description="Task Description for task 5",
                                         developer=self.test_dev_user_2, project=self.test_project,
                                         is_completed=False, final_date=date(9999, 10, 10),
                                         created_by=self.test_pm_user,
                                         updated_by=self.test_pm_user, is_active=False, is_deleted=True)
        response = self.client.get('/api/v1/project-manager/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_post_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_post_request_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 403)

    def test_post_request_with_valid_data_creates_new_task(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 4)

    def test_post_request_with_valid_data_creates_new_task_and_set_code_auto(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 201)
        task = Task.objects.filter(code=response.data['code']).first()
        self.assertTrue(task.code is not None)

    def test_post_request_with_valid_data_sets_created_by_and_updated_by_fields_to_current_user(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        task = Task.objects.filter(code=response.data['code']).first()
        self.assertEqual(task.created_by, self.test_pm_user)
        self.assertEqual(task.updated_by, self.test_pm_user)

    def test_post_request_return_correct_data(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        task = Task.objects.filter(code=response.data['code']).first()
        self.assertEqual(response.data["code"], task.code)
        self.assertEqual(response.data["title"], task.title)
        self.assertEqual(response.data["description"], task.description)
        self.assertEqual(response.data["developer"], task.developer.id)
        self.assertEqual(response.data["is_completed"], task.is_completed)
        self.assertEqual(response.data["final_date"], task.final_date.isoformat())
        self.assertEqual(response.data["is_active"], task.is_active)

    def test_post_request_with_extra_fields_return_correct_data(self):
        data = {
            'code': 'code-0002121',
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12",
            'extra_field': 'Info'
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        task = Task.objects.filter(code=response.data['code']).first()
        self.assertEqual(response.data["code"], task.code)
        self.assertNotEqual('code-0002121', task.code)
        self.assertEqual(response.data["title"], task.title)
        self.assertEqual(response.data["description"], task.description)
        self.assertEqual(response.data["developer"], task.developer.id)
        self.assertEqual(response.data["is_completed"], task.is_completed)
        self.assertEqual(response.data["final_date"], task.final_date.isoformat())
        self.assertEqual(response.data["is_active"], task.is_active)

    def test_post_request_validate_developer_constraint(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 4,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_validate_final_date_constraint(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "2021-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_wrong_project_returns_400(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test endpoints",
            'project': '000000-project',
            'developer': 1,
            'is_completed': False,
            'final_date': "2021-12-12"
        }
        response = self.client.post('/api/v1/project-manager/tasks/', data=data)
        self.assertEqual(response.status_code, 400)


class TestRetrieveUpdateDestroyTask(TestBaseClass):
    """Test /api/v1/project-manager/tasks/code/ endpoint, responses, permissions and constraints"""

    def test_get_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_correct_data(self):
        response = self.client.get('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], self.test_task.code)
        self.assertEqual(response.data["title"], self.test_task.title)
        self.assertEqual(response.data["description"], self.test_task.description)
        self.assertEqual(response.data["developer"], self.test_task.developer.id)
        self.assertEqual(response.data["is_completed"], self.test_task.is_completed)
        self.assertEqual(response.data["final_date"], self.test_task.final_date.isoformat())
        self.assertEqual(response.data["is_active"], self.test_task.is_active)

    def test_get_request_wrong_data_returns_404(self):
        response = self.client.get('/api/v1/project-manager/tasks/0897456-task/')
        self.assertEqual(response.status_code, 404)

    def test_put_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_put_request_authenticated_dev_user_no_task_developer_returns_403(self):
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_request_authenticated_dev_user_task_developer_returns_200(self):
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_request_correct_data_returns_200(self):
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_request_returns_correct_data(self):
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 2,
            'is_completed': True,
            'final_date': "9999-12-10"
        }
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)
        task = Task.objects.filter(code='test-task-01-2024').first()
        self.assertEqual(response.data["code"], self.test_task.code)
        self.assertEqual("Task Updated", task.title)
        self.assertEqual("Task updated to test endpoints", task.description)
        self.assertEqual(self.test_dev_user_2, task.developer)
        self.assertEqual(True, task.is_completed)
        self.assertEqual("9999-12-10", task.final_date.isoformat())
        self.assertEqual(True, task.is_active)

    def test_put_request_auditory_fields_returns_correct_data(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        task = Task.objects.filter(code='test-task-01-2024').first()
        self.assertEqual(task.created_by, self.test_pm_user)
        self.assertEqual(task.updated_by, self.test_pm_user_2)

    def test_put_request_wrong_developer_returns_400(self):
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 4,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_put_request_wrong_final_date_returns_400(self):
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
            'project': 'test-project-01-2024',
            'developer': 4,
            'is_completed': False,
            'final_date': "2021-12-12"
        }
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_patch_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        data = {
            'title': "Task Updated",
            'project': 'test-project-01-2024',
            'developer': 1
        }
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_patch_request_authenticated_dev_user_no_task_developer_returns_403(self):
        data = {
            'title': "Task Updated",
            'project': 'test-project-01-2024',
            'developer': 1
        }
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch_request_authenticated_dev_user_task_developer_returns_200(self):
        data = {
            'title': "Task Updated",
            'project': 'test-project-01-2024',
            'developer': 1
        }
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_request_correct_data_returns_200(self):
        data = {
            'title': "Task Updated",
            'project': 'test-project-01-2024',
            'developer': 1
        }
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_request_returns_correct_data(self):
        data = {
            'title': "Task Updated",
            'developer': 2
        }
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 200)
        task = Task.objects.filter(code='test-task-01-2024').first()
        # Updated fields
        self.assertEqual("Task Updated", task.title)
        self.assertEqual(self.test_dev_user_2, task.developer)
        # Non updated fields
        self.assertEqual(response.data["code"], self.test_task.code)
        self.assertEqual(self.test_task.description, task.description)
        self.assertEqual(self.test_task.is_deleted, task.is_completed)
        self.assertEqual(self.test_task.final_date, task.final_date)
        self.assertEqual(self.test_task.is_active, task.is_active)

    def test_patch_request_auditory_fields_returns_correct_data(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'title': "Task Updated",
            'description': "Task updated to test endpoints",
        }
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        task = Task.objects.filter(code='test-task-01-2024').first()
        self.assertEqual(task.created_by, self.test_pm_user)
        self.assertEqual(task.updated_by, self.test_pm_user_2)

    def test_patch_request_wrong_developer_returns_400(self):
        data = {
            'developer': 4
        }
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_patch_request_wrong_final_date_returns_400(self):
        data = {
            'final_date': "2021-12-12"
        }
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_delete_request_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 401)

    def test_delete_request_authenticated_dev_user_returns_401(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 403)

    def test_delete_request_returns_204(self):
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 204)

    def test_delete_request_update_fields_correctly(self):
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/')
        self.assertEqual(response.status_code, 204)
        task = Task.objects.filter(code='test-task-01-2024').first()
        self.assertEqual(False, task.is_active)
        self.assertEqual(True, task.is_deleted)


class TestListProjectsByProjectManager(TestBaseClass):
    """Test /api/v1/project-manager/projects/<int:project_manager_id> endpoint permissions and responses """

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/projects/4')
        self.assertEqual(response.status_code, 401)

    def test_get_request_dev_user_authenticated_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/project-manager/projects/4')
        self.assertEqual(response.status_code, 403)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/project-manager/projects/4')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_200_and_count_equal_1(self):
        response = self.client.get('/api/v1/project-manager/projects/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_request_dont_returns_list_of_active_and_non_deleted_projects(self):
        new_project = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                             description="Project Description for project 2",
                                             project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user, is_active=False)
        new_project_2 = Project.objects.create(code="test-project-03-2024", name="Test Project 3",
                                               description="Project Description for project 3",
                                               project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user, is_deleted=True)
        response = self.client.get('/api/v1/project-manager/projects/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_request_dont_returns_list_of_another_project_manager_projects(self):
        new_project = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                             description="Project Description for project 2",
                                             project_manager=self.test_pm_user_2, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)
        new_project_2 = Project.objects.create(code="test-project-03-2024", name="Test Project 3",
                                               description="Project Description for project 3",
                                               project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user)
        response = self.client.get('/api/v1/project-manager/projects/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_wrong_user_id_returns_301(self):
        response = self.client.get('/api/v1/project-manager/projects/project')
        self.assertEqual(response.status_code, 301)


class TestListTasksByDeveloper(TestBaseClass):
    """Test /api/v1/project-manager/tasks/<int:developer_id> endpoint responses and permissions"""

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 401)

    def test_get_request_access_authenticated_unrequested_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 403)

    def test_get_request_requested_user_authenticated_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_200_and_count_equal_to_2(self):
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_non_active_and_deleted_tasks(self):
        new_task = Task.objects.create(code="test-task-04-2024", title="Test Task number 4",
                                       description="Task Description for task 4",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(9999, 10, 10),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user, is_active=False, is_deleted=False)
        new_task_2 = Task.objects.create(code="test-task-05-2024", title="Test Task number 5",
                                         description="Task Description for task 5",
                                         developer=self.test_dev_user, project=self.test_project,
                                         is_completed=False, final_date=date(9999, 10, 10),
                                         created_by=self.test_pm_user,
                                         updated_by=self.test_pm_user, is_active=False, is_deleted=True)
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_another_developer_tasks(self):
        new_task = Task.objects.create(code="test-task-04-2024", title="Test Task number 4",
                                       description="Task Description for task 4",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(9999, 10, 10),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        new_task_2 = Task.objects.create(code="test-task-05-2024", title="Test Task number 5",
                                         description="Task Description for task 5",
                                         developer=self.test_dev_user_2, project=self.test_project,
                                         is_completed=False, final_date=date(9999, 10, 10),
                                         created_by=self.test_pm_user,
                                         updated_by=self.test_pm_user)
        response = self.client.get('/api/v1/project-manager/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_wrong_user_id_returns_301(self):
        response = self.client.get('/api/v1/project-manager/tasks/developer')
        self.assertEqual(response.status_code, 301)


class TestListDeveloperTasksInProject(TestBaseClass):
    """Test tasks/<int:developer_id>/<slug:project_code> endpoint responses and permissions"""

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 401)

    def test_get_request_access_authenticated_unrequested_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 403)

    def test_get_request_requested_user_authenticated_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_200_and_count_equal_to_2(self):
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_non_active_and_deleted_tasks(self):
        new_task = Task.objects.create(code="test-task-04-2024", title="Test Task number 4",
                                       description="Task Description for task 4",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(9999, 10, 10),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user, is_active=False, is_deleted=False)
        new_task_2 = Task.objects.create(code="test-task-05-2024", title="Test Task number 5",
                                         description="Task Description for task 5",
                                         developer=self.test_dev_user, project=self.test_project,
                                         is_completed=False, final_date=date(9999, 10, 10),
                                         created_by=self.test_pm_user,
                                         updated_by=self.test_pm_user, is_active=False, is_deleted=True)
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_another_developer_tasks(self):
        new_task = Task.objects.create(code="test-task-04-2024", title="Test Task number 4",
                                       description="Task Description for task 4",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(9999, 10, 10),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        new_task_2 = Task.objects.create(code="test-task-05-2024", title="Test Task number 5",
                                         description="Task Description for task 5",
                                         developer=self.test_dev_user_2, project=self.test_project,
                                         is_completed=False, final_date=date(9999, 10, 10),
                                         created_by=self.test_pm_user,
                                         updated_by=self.test_pm_user)
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_request_dont_returns_list_of_another_project_tasks(self):
        test_project_2 = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                                description="Project 2 Description",
                                                project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                updated_by=self.test_pm_user)
        new_task = Task.objects.create(code="test-task-04-2024", title="Test Task number 4",
                                       description="Task Description for task 4",
                                       developer=self.test_dev_user, project=test_project_2,
                                       is_completed=False, final_date=date(9999, 10, 10),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        response = self.client.get('/api/v1/project-manager/tasks/1/test-project-01-2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_wrong_user_id_returns_400(self):
        response = self.client.get('/api/v1/project-manager/tasks/user-wrong-id/test-project-01-2024')
        self.assertEqual(response.status_code, 404)

    def test_wrong_project_code_returns_404(self):
        response = self.client.get('/api/v1/project-manager/tasks/1/wrong-project-code')
        self.assertEqual(response.status_code, 404)


class TestListAvailableDevelopers(TestBaseClass):
    """Test /api/v1/project-manager/available-developers/ endpoint responses and permissions"""

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/project-manager/available-developers/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_access_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/project-manager/available-developers/')
        self.assertEqual(response.status_code, 403)

    def test_get_request_authenticated_user_returns_200_and_count_equal_to_2(self):
        response = self.client.get('/api/v1/project-manager/available-developers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_request_with_available_dev_users_return_correct_count(self):
        self.test_dev_user = User.objects.create_user(id=6,
                                                      email='cris@gmail.com',
                                                      first_name='Christian',
                                                      last_name='Brown',
                                                      role='D',
                                                      mobile_phone='+1 87451233',
                                                      password='SecurePass78*01')
        self.test_dev_user = User.objects.create_user(id=7,
                                                      email='patrick@gmail.com',
                                                      first_name='Patrick',
                                                      last_name='Wallace',
                                                      role='D',
                                                      mobile_phone='+52 887741222',
                                                      password='SecurePass78*01')
        self.test_dev_user = User.objects.create_user(id=8,
                                                      email='zuko@gmail.com',
                                                      first_name='Zuko',
                                                      last_name='Kenwood',
                                                      role='P',
                                                      mobile_phone='+11 787878743',
                                                      password='SecurePass78*01')
        response = self.client.get('/api/v1/project-manager/available-developers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_request_dont_returns_list_of_non_active_and_deleted_dev_users(self):
        self.test_dev_user = User.objects.create_user(id=6,
                                                      email='cris@gmail.com',
                                                      first_name='Christian',
                                                      last_name='Brown',
                                                      role='D',
                                                      mobile_phone='+1 87451233',
                                                      password='SecurePass78*01',
                                                      is_active=False,
                                                      )
        self.test_dev_user = User.objects.create_user(id=7,
                                                      email='patrick@gmail.com',
                                                      first_name='Patrick',
                                                      last_name='Wallace',
                                                      role='D',
                                                      mobile_phone='+52 887741222',
                                                      password='SecurePass78*01',
                                                      deleted=True)
        self.test_dev_user = User.objects.create_user(id=8,
                                                      email='zuko@gmail.com',
                                                      first_name='Zuko',
                                                      last_name='Kenwood',
                                                      role='D',
                                                      mobile_phone='+11 787878743',
                                                      password='SecurePass78*01')
        response = self.client.get('/api/v1/project-manager/available-developers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class TestEnableProject(TestBaseClass):
    """Test /api/v1/project-manager/projects/<slug:code>/enable endpoint"""

    def test_put_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/enable')
        self.assertEqual(response.status_code, 401)

    def test_put_request_access_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.put('/api/v1/project-manager/projects/test-project-01-2024/enable')
        self.assertEqual(response.status_code, 403)

    def test_patch_request_authenticated_correct_user_returns_405(self):
        response = self.client.patch('/api/v1/project-manager/projects/test-project-01-2024/enable')
        self.assertEqual(response.status_code, 405)

    def test_put_request_authenticated_user_returns_200(self):
        self.test_project_2 = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                                     description="Project 2 Description",
                                                     project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                     updated_by=self.test_pm_user, is_active=False, is_deleted=False)
        response = self.client.put('/api/v1/project-manager/projects/test-project-02-2024/enable')
        self.assertEqual(response.status_code, 200)

    def test_put_request_activates_correctly_a_project(self):
        self.test_project_2 = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                                     description="Project 2 Description",
                                                     project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                     updated_by=self.test_pm_user, is_active=False, is_deleted=False)
        self.assertEqual(Project.objects.filter(is_active=True).count(), 1)
        response = self.client.put('/api/v1/project-manager/projects/test-project-02-2024/enable')
        self.assertEqual(Project.objects.filter(is_active=True).count(), 2)

    def test_put_request_cant_activate_a_project_already_active(self):
        self.test_project_2 = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                                     description="Project 2 Description",
                                                     project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                     updated_by=self.test_pm_user, is_active=True, is_deleted=False)
        response = self.client.put('/api/v1/project-manager/projects/test-project-02-2024/enable')
        self.assertEqual(response.status_code, 404)


class TestDisableProject(TestBaseClass):
    """Test /api/v1/project-manager/projects/<slug:code>/disable endpoint"""

    def test_delete_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/disable')
        self.assertEqual(response.status_code, 401)

    def test_delete_request_access_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/disable')
        self.assertEqual(response.status_code, 403)

    def test_delete_request_authenticated_user_returns_200(self):
        response = self.client.delete('/api/v1/project-manager/projects/test-project-01-2024/disable')
        self.assertEqual(response.status_code, 204)

    def test_delete_request_deactivate_correctly_a_project(self):
        self.test_project_2 = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                                     description="Project 2 Description",
                                                     project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                     updated_by=self.test_pm_user, is_active=True, is_deleted=False)
        self.assertEqual(Project.objects.filter(is_active=True).count(), 2)
        response = self.client.delete('/api/v1/project-manager/projects/test-project-02-2024/disable')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Project.objects.filter(is_active=True).count(), 1)

    def test_delete_request_cant_activate_a_project_already_active(self):
        self.test_project_2 = Project.objects.create(code="test-project-02-2024", name="Test Project 2",
                                                     description="Project 2 Description",
                                                     project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                     updated_by=self.test_pm_user, is_active=False, is_deleted=False)
        response = self.client.delete('/api/v1/project-manager/projects/test-project-02-2024/disable')
        self.assertEqual(response.status_code, 404)


class TestEnableTask(TestBaseClass):
    """Test /api/v1/project-manager/tasks/<slug:code>/enable endpoint"""

    def test_put_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/enable')
        self.assertEqual(response.status_code, 401)

    def test_put_request_access_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.put('/api/v1/project-manager/tasks/test-task-01-2024/enable')
        self.assertEqual(response.status_code, 403)

    def test_patch_request_authenticated_correct_user_returns_405(self):
        response = self.client.patch('/api/v1/project-manager/tasks/test-task-01-2024/enable')
        self.assertEqual(response.status_code, 405)

    def test_put_request_authenticated_user_returns_200(self):
        self.test_task_4 = Task.objects.create(code="test-task-04-2024", title="Test Task 4",
                                               description="Task 4 Description",
                                               developer=self.test_dev_user, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user,
                                               is_active=False, is_deleted=False)
        response = self.client.put('/api/v1/project-manager/tasks/test-task-04-2024/enable')
        self.assertEqual(response.status_code, 200)

    def test_put_request_activates_correctly_a_project(self):
        self.test_task_4 = Task.objects.create(code="test-task-04-2024", title="Test Task 4",
                                               description="Task 4 Description",
                                               developer=self.test_dev_user, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user,
                                               is_active=False, is_deleted=False)
        self.assertEqual(Task.objects.filter(is_active=True).count(), 3)
        response = self.client.put('/api/v1/project-manager/tasks/test-task-04-2024/enable')
        self.assertEqual(Task.objects.filter(is_active=True).count(), 4)

    def test_put_request_cant_activate_a_project_already_active(self):
        self.test_task_4 = Task.objects.create(code="test-task-04-2024", title="Test Task 4",
                                               description="Task 4 Description",
                                               developer=self.test_dev_user, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user,
                                               is_active=True, is_deleted=False)
        response = self.client.put('/api/v1/project-manager/tasks/test-task-04-2024/enable')
        self.assertEqual(response.status_code, 404)


class TestDisableTask(TestBaseClass):
    """Test /api/v1/project-manager/tasks/<slug:code>/disable endpoint"""

    def test_delete_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/disable')
        self.assertEqual(response.status_code, 401)

    def test_delete_request_access_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/disable')
        self.assertEqual(response.status_code, 403)

    def test_delete_request_authenticated_user_returns_200(self):
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-01-2024/disable')
        self.assertEqual(response.status_code, 204)

    def test_delete_request_activates_correctly_a_project(self):
        self.test_task_4 = Task.objects.create(code="test-task-04-2024", title="Test Task 4",
                                               description="Task 4 Description",
                                               developer=self.test_dev_user, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user,
                                               is_active=True, is_deleted=False)
        self.assertEqual(Task.objects.filter(is_active=True).count(), 4)
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-04-2024/disable')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.filter(is_active=True).count(), 3)

    def test_delete_request_cant_activate_a_project_already_active(self):
        self.test_task_4 = Task.objects.create(code="test-task-04-2024", title="Test Task 4",
                                               description="Task 4 Description",
                                               developer=self.test_dev_user, project=self.test_project,
                                               is_completed=False, final_date=date(9999, 10, 10),
                                               created_by=self.test_pm_user,
                                               updated_by=self.test_pm_user,
                                               is_active=False, is_deleted=False)
        response = self.client.delete('/api/v1/project-manager/tasks/test-task-04-2024/disable')
        self.assertEqual(response.status_code, 404)
