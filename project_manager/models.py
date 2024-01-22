from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .reference_model import Auditory
from .utils import generate_unique_slug_code, email_purpose
from .validators import validate_user_is_project_manager, validate_user_is_developer

User = get_user_model()

# Create your models here.


class Project(Auditory):
    # Code creation is handled by save() method.
    code = models.SlugField(unique=True, max_length=50, verbose_name='Code')
    name = models.CharField(max_length=200, verbose_name='Project name')
    description = models.TextField(verbose_name='Project Description')
    project_manager = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                        related_name='projects', validators=[validate_user_is_project_manager, ])
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='projects_created')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='projects_updated')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at', ]

    def __str__(self):
        return self.code

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.code:
            self.code = generate_unique_slug_code(name=self.name, model=Project)
        super().save()


class Task(Auditory):
    # Code creation is handled by a signal
    code = models.SlugField(unique=True, max_length=50, verbose_name='Code')
    title = models.CharField(max_length=200, verbose_name='Task title')
    description = models.TextField(verbose_name='Task Description')
    developer = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                  related_name='tasks', verbose_name='Developer',
                                  validators=[validate_user_is_developer, ])
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='tasks', verbose_name='Project')
    is_completed = models.BooleanField(default=False)
    final_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tasks_created')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tasks_updated')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at', ]

    def clean(self):
        if self.final_date < timezone.now().date():
            raise ValidationError(f"The final date must be a future date, {self.final_date} is before today")

    def __str__(self):
        return self.code


class EmailLog(models.Model):
    # Redundancy added to reduce database query
    destination_email = models.EmailField(unique=False, verbose_name='Destination Email')
    email_purpose = models.CharField(max_length=1, choices=email_purpose, verbose_name='Email Purpose')
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, verbose_name='Task')
    delivered = models.BooleanField(default=False, verbose_name='Delivered')
    error_info = models.TextField(blank=True, null=True, verbose_name='Error Info')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-created_at', ]

    def __str__(self):
        return f"email log {self.pk}"
