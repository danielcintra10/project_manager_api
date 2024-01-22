from django.core.mail import send_mail
from django.db.models.functions import Now
from core import settings
from .models import EmailLog, Task
from celery import shared_task


@shared_task
def send_email_to_developer_user_after_new_task_created(task_code):
    task = Task.objects.filter(code=task_code).first()
    try:
        subject = f"New Task from project {task.project.name}"
        message = f"Hello, you have a new task assigned to the project {task.project.name}, \n " \
                  f"the title is {task.title}. \n " \
                  f"I give you a description of what it is about: \n" \
                  f"{task.description}, \n \n" \
                  f"the deadline to complete this task is: {task.final_date} \n" \
                  f"Have a nice day"
        from_email = task.project.project_manager.email
        recipient_list = [task.developer.email, ]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        email_log = EmailLog.objects.create(destination_email=task.developer.email,
                                            email_purpose="C",
                                            task=task,
                                            delivered=True,
                                            error_info=None,
                                            )
    except Exception as e:
        email_log = EmailLog.objects.create(destination_email=task.developer.email,
                                            email_purpose="C",
                                            task=task,
                                            delivered=False,
                                            error_info=str(e),
                                            )


@shared_task
def send_email_to_project_manager_if_task_has_reached_its_deadline():
    tasks = Task.objects.filter(is_active=True, is_deleted=False,
                                is_completed=False, final_date=Now().date())
    for task in tasks:
        try:
            subject = f"Task has reached its deadline"
            message = f"The task {task.title} has reached its deadline. \n" \
                      f"The developer in charge of completing it is " \
                      f"{task.developer.first_name} {task.developer.last_name} \n \n" \
                      f"Developer email {task.developer.email}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [task.project.project_manager.email, ]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            email_log = EmailLog.objects.create(destination_email=task.project.project_manager.email,
                                                email_purpose="F",
                                                task=task,
                                                delivered=True,
                                                error_info=None,
                                                )
        except Exception as e:
            email_log = EmailLog.objects.create(destination_email=task.project.project_manager.email,
                                                email_purpose="F",
                                                task=task,
                                                delivered=False,
                                                error_info=str(e),
                                                )
