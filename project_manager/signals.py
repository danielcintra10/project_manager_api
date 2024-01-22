from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Task
from .utils import generate_unique_slug_code
from .tasks import send_email_to_developer_user_after_new_task_created


@receiver(pre_save, sender=Task)
def set_slug_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = generate_unique_slug_code(name=instance.title, model=Task)


@receiver(post_save, sender=Task)
def activate_async_task(sender, instance, created, *args, **kwargs):
    # This condition allows the email to be sent only in case of the creation of a new instance.
    if created:
        email = send_email_to_developer_user_after_new_task_created.delay(instance.code)
