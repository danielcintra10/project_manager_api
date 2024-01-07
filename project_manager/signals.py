from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from .utils import generate_unique_slug_code


@receiver(pre_save, sender=Task)
def set_slug_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = generate_unique_slug_code(name=instance.title, model=Task)


