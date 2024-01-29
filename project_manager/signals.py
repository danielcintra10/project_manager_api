from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Task, Project
from .utils import generate_unique_slug_code
from .tasks import send_email_to_developer_user_after_new_task_created


def clear_cache(prefix):
    cache_pattern = cache.keys("*" + prefix + "*")
    delete_cache = cache.delete_many(cache_pattern)


@receiver(post_save, sender=Project)
def clear_project_cache(sender, instance, **kwargs):
    clear_cache("project")


@receiver(pre_save, sender=Task)
def set_slug_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = generate_unique_slug_code(
            name=instance.title, model=Task
        )


@receiver(post_save, sender=Task)
def activate_async_task(sender, instance, created, *args, **kwargs):
    # This condition allows the email to be sent only in case of the creation of a new instance.
    if created:
        email = send_email_to_developer_user_after_new_task_created.delay(
            instance.code
        )


@receiver(post_save, sender=Task)
def clear_task_and_project_cache(sender, instance, **kwargs):
    # In this case if a task is updated the project is updated
    clear_cache("task")
    clear_cache("project")
