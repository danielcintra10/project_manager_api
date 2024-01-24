from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Command to configure periodic tasks using django-celery-beat"

    def handle(self, *args, **options):
        # Get or create schedule.
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="9",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )
        # The condition is used to prevent repeated tasks, in case the user executes this command more than once.
        task = PeriodicTask.objects.filter(
            name="Completed task finder"
        ).first()
        if not task:
            PeriodicTask.objects.create(
                crontab=schedule,
                name="Completed task finder",
                task="project_manager.tasks.send_email_to_project_manager_if_task_has_reached_its_deadline",
            )
            print(
                "Task configured successfully, you dont need to run this command again"
            )
        print(
            "The task was previously configured, you dont need to run this command again"
        )
