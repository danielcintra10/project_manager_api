from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


def clear_user_cache():
    user_cache = cache.keys("*user*")
    delete_cache = cache.delete_many(user_cache)


@receiver(post_save, sender=User)
def clear_cache(sender, instance, **kwargs):
    clear_user_cache()
