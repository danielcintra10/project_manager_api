from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from datetime import date
from project_manager.models import Project, Task
from api.serializers import ProjectSerializer, TaskSerializer


User = get_user_model()


class BaseSerializersClass(TestCase):
    """Base class to test Project and Task serializers"""
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

        self.test_pm_user_2 = User.objects.create_user(id=3,
                                                       email='pmusermail@gmail.com',
                                                       first_name='Jenni',
                                                       last_name='Doe',
                                                       role='P',
                                                       mobile_phone='+34 879888100',
                                                       password='password*strong23')

        self.test_project = Project.objects.create(code="test-project-012024", name="Test Project",
                                                   description="Project Description",
                                                   project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                   updated_by=self.test_pm_user)

        self.test_task = Task.objects.create(code="test-task-012024", title="Test Task", description="Task Description",
                                             developer=self.test_dev_user, project=self.test_project,
                                             is_completed=False, final_date=date(9999, 10, 10),
                                             created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)

        self.request = HttpRequest()
        self.request.user = self.test_pm_user


class TestProjectSerializer(BaseSerializersClass):
    """Test if ProjectSerializer work properly"""

    def test_serialize_with_valid_data(self):
        project = Project.objects.filter(code="test-project-012024").first()
        serializer = ProjectSerializer(project, many=False)
        self.assertEqual('test-project-012024', serializer.data.get("code"))
        self.assertEqual('Test Project', serializer.data.get("name"))
        self.assertEqual('Project Description', serializer.data.get("description"))
        self.assertEqual(2, serializer.data.get("project_manager"))
        self.assertTrue(serializer.data.get("is_active"))
        self.assertTrue("tasks" in serializer.data)
        self.assertTrue("created_at" in serializer.data)
        self.assertTrue("updated_at" in serializer.data)

    def test_auditory_fields(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 2
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_project = serializer.save()
        self.assertEqual(self.test_pm_user, new_project.created_by)
        self.assertEqual(self.test_pm_user, new_project.updated_by)

    def test_deserialize_data_ok(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 2
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_project = serializer.save()
        self.assertEqual('New Project Created', new_project.name)
        self.assertEqual('Project created to test serializers', new_project.description)
        self.assertEqual(self.test_pm_user, new_project.project_manager)
        self.assertTrue(new_project.is_active)
        self.assertFalse(new_project.is_deleted)
        self.assertEqual(self.test_pm_user, new_project.created_by)
        self.assertEqual(self.test_pm_user, new_project.updated_by)

    def test_update_instance_with_valid_data(self):
        project = Project.objects.filter(code="test-project-012024").first()
        data = {
            'name': "New name to project",
            'description': "Updated project description",
            'project_manager': 2
        }
        serializer = ProjectSerializer(instance=project, data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        project = serializer.save()
        # Updated fields
        self.assertEqual('New name to project', project.name)
        self.assertEqual('Updated project description', project.description)
        # Non updated fields
        self.assertEqual(self.test_pm_user, project.project_manager)
        self.assertTrue(project.is_active)
        self.assertFalse(project.is_deleted)
        self.assertEqual(self.test_pm_user, project.created_by)
        self.assertEqual(self.test_pm_user, project.updated_by)

    def test_update_instance_with_partial_data(self):
        project = Project.objects.filter(code="test-project-012024").first()
        data = {
            'name': "New name to project",
        }
        serializer = ProjectSerializer(instance=project, data=data, partial=True, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        project = serializer.save()
        # updated fields
        self.assertEqual('New name to project', project.name)
        # non updated fields
        self.assertEqual('Project Description', project.description)
        self.assertEqual(self.test_pm_user, project.project_manager)
        self.assertTrue(project.is_active)
        self.assertFalse(project.is_deleted)
        self.assertEqual(self.test_pm_user, project.created_by)
        self.assertEqual(self.test_pm_user, project.updated_by)

    def test_updated_by_field_when_update(self):
        project = Project.objects.filter(code="test-project-012024").first()
        data = {
            'name': "New name to project",
        }
        self.request.user = self.test_pm_user_2
        serializer = ProjectSerializer(instance=project, data=data, partial=True, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        project = serializer.save()
        self.assertEqual(self.test_pm_user, project.created_by)
        self.assertEqual(self.test_pm_user_2, project.updated_by)

    def test_read_only_fields_not_when_deserialize(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 2
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        with self.assertRaises(KeyError):
            code = serializer.validated_data["code"]
            is_active = serializer.validated_data["is_active"]
            creation_date = serializer.validated_data["created_at"]
            last_update = serializer.validated_data["updated_at"]

    def test_save_project_code_field_created_ok(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 2
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_project = serializer.save()
        self.assertTrue(new_project.code is not None)

    def test_save_project_with_extra_fields_are_not_taken(self):
        data = {
            'code': "code-05478",
            'is_active': False,
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 2
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_project = serializer.save()
        self.assertEqual('New Project Created', new_project.name)
        self.assertEqual('Project created to test serializers', new_project.description)
        self.assertEqual(self.test_pm_user, new_project.project_manager)
        # Fields not taken in count
        self.assertTrue(new_project.is_active)
        self.assertNotEqual('code-05478', new_project.code)

    def test_project_manager_constraint(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 1
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())

    def test_relational_field_developer_created_with_invalid_data_is_not_valid(self):
        data = {
            'name': "New Project Created",
            'description': "Project created to test serializers",
            'project_manager': 'robert@gmail.com'
        }
        serializer = ProjectSerializer(data=data, context={"request": self.request, })
        self.assertFalse(serializer.is_valid())


class TestTaskSerializer(BaseSerializersClass):
    """Test if TaskSerializer work properly"""

    def test_serialize_with_valid_data(self):
        task = Task.objects.filter(code="test-task-012024").first()
        serializer = TaskSerializer(task, many=False, context={'fields': True})
        self.assertEqual('test-task-012024', serializer.data.get("code"))
        self.assertEqual('Test Task', serializer.data.get("title"))
        self.assertEqual('Task Description', serializer.data.get("description"))
        self.assertEqual("test-project-012024", serializer.data.get("project"))
        self.assertEqual(1, serializer.data.get("developer"))
        self.assertFalse(serializer.data.get("is_completed"))
        self.assertEqual(date(9999, 10, 10).isoformat(), serializer.data.get("final_date"))
        self.assertTrue(serializer.data.get("is_active"))
        self.assertTrue("created_at" in serializer.data)
        self.assertTrue("updated_at" in serializer.data)

    def test_serialize_with_valid_data_without_context_dont_show_project_field(self):
        task = Task.objects.filter(code="test-task-012024").first()
        serializer = TaskSerializer(task, many=False, )
        self.assertTrue("project" not in serializer.data)

    def test_auditory_fields(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_task = serializer.save()
        self.assertEqual(self.test_pm_user, new_task.created_by)
        self.assertEqual(self.test_pm_user, new_task.updated_by)

    def test_deserialize_data_ok(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_task = serializer.save()
        self.assertEqual('New Task Created', new_task.title)
        self.assertEqual('Task created to test serializers', new_task.description)
        self.assertEqual(self.test_project, new_task.project)
        self.assertEqual(self.test_dev_user, new_task.developer)
        self.assertFalse(new_task.is_completed)
        self.assertEqual("9999-12-12", new_task.final_date.isoformat())
        self.assertTrue(new_task.is_active)
        self.assertEqual(self.test_pm_user, new_task.created_by)
        self.assertEqual(self.test_pm_user, new_task.updated_by)

    def test_update_instance_with_valid_data(self):
        task = Task.objects.filter(code="test-task-012024").first()
        data = {
            'title': "Task updated",
            'description': "Task updated to test serializers",
            'project': 'test-project-012024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-06-04"
        }
        serializer = TaskSerializer(instance=task, data=data, context={"request": self.request, "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        task = serializer.save()
        # Updated fields
        self.assertEqual('Task updated', task.title)
        self.assertEqual('Task updated to test serializers', task.description)
        self.assertEqual(self.test_project, task.project)
        self.assertEqual("9999-06-04", task.final_date.isoformat())
        # Non updated fields
        self.assertEqual(self.test_dev_user, task.developer)
        self.assertFalse(task.is_completed)
        self.assertTrue(task.is_active)
        self.assertEqual(self.test_pm_user, task.created_by)
        self.assertEqual(self.test_pm_user, task.updated_by)

    def test_update_instance_with_partial_data(self):
        task = Task.objects.filter(code="test-task-012024").first()
        data = {
            'title': "Task updated",
            'is_completed': True,
        }
        serializer = TaskSerializer(instance=task, data=data, partial=True, context={"request": self.request, "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        task = serializer.save()
        # Updated fields
        self.assertEqual('Task updated', task.title)
        self.assertTrue(task.is_completed)
        # Non updated fields
        self.assertEqual('Task Description', task.description)
        self.assertEqual(self.test_project, task.project)
        self.assertEqual("9999-10-10", task.final_date.isoformat())
        self.assertEqual(self.test_dev_user, task.developer)
        self.assertTrue(task.is_active)
        self.assertEqual(self.test_pm_user, task.created_by)
        self.assertEqual(self.test_pm_user, task.updated_by)

    def test_updated_by_field_when_update(self):
        task = Task.objects.filter(code="test-task-012024").first()
        data = {
            'title': "Task updated",
        }
        self.request.user = self.test_pm_user_2
        serializer = TaskSerializer(instance=task, data=data, partial=True, context={"request": self.request,
                                                                                     "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        task = serializer.save()
        self.assertEqual(self.test_pm_user, task.created_by)
        self.assertEqual(self.test_pm_user_2, task.updated_by)

    def test_read_only_fields_not_when_deserialize(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        with self.assertRaises(KeyError):
            code = serializer.validated_data["code"]
            is_active = serializer.validated_data["is_active"]
            creation_date = serializer.validated_data["created_at"]
            last_update = serializer.validated_data["updated_at"]

    def test_if_code_field_is_created_ok(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_task = serializer.save()
        self.assertTrue(new_task.code is not None)

    def test_save_project_with_extra_fields_are_not_taken(self):
        data = {
            'code': 'test-7878778',
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 1,
            'is_completed': False,
            'final_date': "9999-12-12",
            'is_active': False
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        new_task = serializer.save()
        # Fields not taken in count
        self.assertTrue(new_task.is_active)
        self.assertNotEqual('test-7878778', new_task.code)

    def test_task_developer_constraint(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 2,
            'is_completed': False,
            'final_date': "9999-12-12"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertFalse(serializer.is_valid())

    def test_task_final_date_constraint(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 2,
            'is_completed': False,
            'final_date': "2022-01-16"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertFalse(serializer.is_valid())

    def test_relational_field_project_created_with_invalid_data_is_not_valid(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 1,
            'developer': 2,
            'is_completed': False,
            'final_date': "2022-01-16"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertFalse(serializer.is_valid())

    def test_relational_field_developer_created_with_invalid_data_is_not_valid(self):
        data = {
            'title': "New Task Created",
            'description': "Task created to test serializers",
            'project': 'test-project-012024',
            'developer': 'robert@gmail.com',
            'is_completed': False,
            'final_date': "2022-01-16"
        }
        serializer = TaskSerializer(data=data, context={"request": self.request, "fields": True})
        self.assertFalse(serializer.is_valid())
