from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date
from project_manager.models import Project, Task, EmailLog

User = get_user_model()


class TestProject(TestCase):
    """Test Project model to check work properly"""

    def setUp(self):
        self.test_dev_user = User.objects.create_user(email='robert@gmail.com',
                                                      first_name='Robert',
                                                      last_name='Lopez',
                                                      role='D',
                                                      mobile_phone='+53 59876543',
                                                      password='1234')

        self.test_pm_user = User.objects.create_user(email='dany@gmail.com',
                                                     first_name='Daniel',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 54876543',
                                                     password='fcb')

        self.test_project = Project.objects.create(name="Test Project", description="Project Description",
                                                   project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                   updated_by=self.test_pm_user)

    def test_code_field_is_completed_correctly_when_save_new_projects(self):
        new_project = Project.objects.create(name="Second Project Created", description="Description of the project",
                                             project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)
        if not new_project.code:
            with self.assertRaises(Exception):
                raise ValueError

    def test_code_field_wont_change_when_update_projects(self):
        new_project = Project.objects.create(name="Second Project Created", description="Description of the project",
                                             project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)
        project = Project.objects.filter(code=new_project.code).first()
        project.name = "New name to the project"
        project.save()
        self.assertEqual(new_project.code, project.code)
        self.assertNotEqual(new_project.name, project.name)

    def test_create_new_project_with_valid_data(self):
        new_project = Project.objects.create(name="Second Project Created", description="Description of the project",
                                             project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)
        project = Project.objects.filter(code=new_project.code).first()
        data = {
            "code": new_project.code,
            "name": "Second Project Created",
            "description": "Description of the project",
            "project_manager": self.test_pm_user,
            "created_by": self.test_pm_user,
            "updated_by": self.test_pm_user,
            "is_active": True,
            "is_deleted": False,
        }
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(data, {
            "code": project.code,
            "name": project.name,
            "description": project.description,
            "project_manager": project.project_manager,
            "created_by": project.created_by,
            "updated_by": project.updated_by,
            "is_active": project.is_active,
            "is_deleted": project.is_deleted,
        })

    def test_update_project_with_valid_data(self):
        self.test_project.name = "New Project name"
        self.test_project.description = "New Project Description"
        self.test_project.is_active = False
        self.test_project.save()
        project = Project.objects.filter(code=self.test_project.code).first()
        data = {
            "code": self.test_project.code,
            "name": "New Project name",
            "description": "New Project Description",
            "project_manager": self.test_pm_user,
            "created_by": self.test_pm_user,
            "updated_by": self.test_pm_user,
            "is_active": False,
            "is_deleted": False,
        }
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(data, {
            "code": project.code,
            "name": project.name,
            "description": project.description,
            "project_manager": project.project_manager,
            "created_by": project.created_by,
            "updated_by": project.updated_by,
            "is_active": project.is_active,
            "is_deleted": project.is_deleted,
        })

    def test_error_when_create_a_project_with_missing_fields(self):
        with self.assertRaises(Exception):
            new_project = Project.objects.create(name="Second Project Created",
                                                 description="Description of the project", )

    def test_delete_project(self):
        new_project = Project.objects.create(name="Second Project Created", description="Description of the project",
                                             project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)
        self.assertEqual(Project.objects.count(), 2)
        project = Project.objects.filter(code=new_project.code).first()
        project.delete()
        self.assertEqual(Project.objects.count(), 1)
        self.assertFalse(Project.objects.filter(code__exact=new_project.code).exists())

    def test_code_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            new_project = Project.objects.create(code=self.test_project.code,
                                                 name="Second Project Created",
                                                 description="Description of the project",
                                                 project_manager=self.test_pm_user,
                                                 created_by=self.test_pm_user,
                                                 updated_by=self.test_pm_user)

    def test_validate_only_project_managers_in_project_manager_field(self):
        with self.assertRaises(ValidationError):
            new_project = Project(name="Second Project Created", description="Description of the project",
                                  project_manager=self.test_dev_user, created_by=self.test_pm_user,
                                  updated_by=self.test_pm_user)
            new_project.full_clean()
            new_project.save()


class TestTask(TestCase):
    """Test Task model to check work properly"""

    def setUp(self):
        self.test_dev_user = User.objects.create_user(email='robert@gmail.com',
                                                      first_name='Robert',
                                                      last_name='Lopez',
                                                      role='D',
                                                      mobile_phone='+53 59876543',
                                                      password='1234')

        self.test_pm_user = User.objects.create_user(email='dany@gmail.com',
                                                     first_name='Daniel',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 54876543',
                                                     password='fcb')

        self.test_project = Project.objects.create(name="Test Project", description="Project Description",
                                                   project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                   updated_by=self.test_pm_user)

        self.test_task = Task.objects.create(title="Test Task", description="Task Description",
                                             developer=self.test_dev_user, project=self.test_project,
                                             is_completed=False, final_date=date(2023, 1, 30),
                                             created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)

    def test_pre_save_signal_to_complete_code_field_works_correctly(self):
        new_task = Task.objects.create(title="Second Task created", description="Task very big Description",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(2023, 1, 30),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        if not new_task.code:
            with self.assertRaises(Exception):
                raise ValueError

    def test_code_field_wont_change_when_update_tasks(self):
        new_task = Task.objects.create(title="Second Task created", description="Task very big Description",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(2023, 1, 30),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        task = Task.objects.filter(code=new_task.code).first()
        task.title = "New title to the Task"
        task.save()
        self.assertEqual(new_task.code, task.code)
        self.assertNotEqual(new_task.title, task.title)

    def test_create_new_task_with_valid_data(self):
        new_task = Task.objects.create(title="Second Task created", description="Task very big Description",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(2023, 1, 30),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        data = {
            "code": new_task.code,
            "title": "Second Task created",
            "description": "Task very big Description",
            "developer": self.test_dev_user,
            "project": self.test_project,
            "is_completed": False,
            "final_date": date(2023, 1, 30),
            "created_by": self.test_pm_user,
            "updated_by": self.test_pm_user,
            "is_active": True,
            "is_deleted": False,
        }
        task = Task.objects.filter(code=new_task.code).first()
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(data, {
            "code": task.code,
            "title": task.title,
            "description": task.description,
            "developer": task.developer,
            "project": task.project,
            "is_completed": task.is_completed,
            "final_date": task.final_date,
            "created_by": task.created_by,
            "updated_by": task.updated_by,
            "is_active": task.is_active,
            "is_deleted": task.is_deleted,
        })

    def test_update_task_with_valid_data(self):
        self.test_task.title = "Updated title"
        self.test_task.description = "Description updated"
        self.test_task.final_date = date(2023, 1, 20)
        self.test_task.is_completed = True
        self.test_task.save()
        data = {
            "code": self.test_task.code,
            "title": "Updated title",
            "description": "Description updated",
            "developer": self.test_dev_user,
            "project": self.test_project,
            "is_completed": True,
            "final_date": date(2023, 1, 20),
            "created_by": self.test_pm_user,
            "updated_by": self.test_pm_user,
            "is_active": True,
            "is_deleted": False,
        }
        task = Task.objects.filter(code=self.test_task.code).first()
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(data, {
            "code": task.code,
            "title": task.title,
            "description": task.description,
            "developer": task.developer,
            "project": task.project,
            "is_completed": task.is_completed,
            "final_date": task.final_date,
            "created_by": task.created_by,
            "updated_by": task.updated_by,
            "is_active": task.is_active,
            "is_deleted": task.is_deleted,
        })

    def test_error_when_create_a_task_with_missing_fields(self):
        with self.assertRaises(Exception):
            new_task = Project.objects.create(title="Second Project Created",
                                              developer=self.test_dev_user, )

    def test_delete_task(self):
        new_task = Task.objects.create(title="Second Task created", description="Task very big Description",
                                       developer=self.test_dev_user, project=self.test_project,
                                       is_completed=False, final_date=date(2023, 1, 30),
                                       created_by=self.test_pm_user,
                                       updated_by=self.test_pm_user)
        self.assertEqual(Task.objects.count(), 2)
        task = Task.objects.filter(code=new_task.code).first()
        task.delete()
        self.assertEqual(Task.objects.count(), 1)
        self.assertFalse(Task.objects.filter(code__exact=new_task.code).exists())

    def test_code_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            new_task = Task.objects.create(code=self.test_task.code, title="Second Task created",
                                           description="Task very big Description",
                                           developer=self.test_dev_user, project=self.test_project,
                                           is_completed=False, final_date=date(2023, 1, 30),
                                           created_by=self.test_pm_user,
                                           updated_by=self.test_pm_user)

    def test_validate_only_developer_users_in_developer_field(self):
        with self.assertRaises(ValidationError):
            new_task = Task.objects.create(title="Second Task created", description="Task very big Description",
                                           developer=self.test_pm_user, project=self.test_project,
                                           is_completed=False, final_date=date(2023, 1, 30),
                                           created_by=self.test_pm_user,
                                           updated_by=self.test_pm_user)
            new_task.full_clean()

    def test_create_task_with_final_date_before_creation_date_return_validation_error(self):
        with self.assertRaises(ValidationError):
            new_task = Task.objects.create(title="Second Task created", description="Task very big Description",
                                           developer=self.test_pm_user, project=self.test_project,
                                           is_completed=False, final_date=date(2022, 10, 10),
                                           created_by=self.test_pm_user,
                                           updated_by=self.test_pm_user)
            new_task.full_clean()


class TestEmailLog(TestCase):
    """Test EmailLog model to check if works properly"""

    def setUp(self):
        self.test_dev_user = User.objects.create_user(email='robert@gmail.com',
                                                      first_name='Robert',
                                                      last_name='Lopez',
                                                      role='D',
                                                      mobile_phone='+53 59876543',
                                                      password='1234')

        self.test_pm_user = User.objects.create_user(email='dany@gmail.com',
                                                     first_name='Daniel',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 54876543',
                                                     password='fcb')

        self.test_project = Project.objects.create(name="Test Project", description="Project Description",
                                                   project_manager=self.test_pm_user, created_by=self.test_pm_user,
                                                   updated_by=self.test_pm_user)

        self.test_task = Task.objects.create(title="Test Task", description="Task Description",
                                             developer=self.test_dev_user, project=self.test_project,
                                             is_completed=False, final_date=date(2023, 1, 30),
                                             created_by=self.test_pm_user,
                                             updated_by=self.test_pm_user)

    def test_create_new_email_log_with_valid_data(self):
        email_log = EmailLog.objects.create(destination_email=self.test_dev_user.email,
                                            email_purpose="C",
                                            task=self.test_task,
                                            delivered=True,
                                            )
        self.assertEqual(EmailLog.objects.count(), 1)

    def test_create_new_email_log_returns_correct_data(self):
        email_log = EmailLog.objects.create(destination_email=self.test_dev_user.email,
                                            email_purpose="C",
                                            task=self.test_task,
                                            delivered=True,
                                            )
        self.assertEqual(EmailLog.objects.count(), 1)
        log = EmailLog.objects.first()
        self.assertEqual(log.destination_email, self.test_dev_user.email)
        self.assertEqual(log.email_purpose, "C")
        self.assertEqual(log.task, self.test_task)
        self.assertEqual(log.delivered, True)
        self.assertEqual(log.error_info, None)

    def test_error_when_create_a_email_log_with_missing_fields(self):
        with self.assertRaises(Exception):
            email_log = EmailLog.objects.create(destination_email=self.test_dev_user.email,
                                                delivered=True,
                                                )
