from django.utils.text import slugify
import uuid


def generate_slug(name):
    """Generate a slug based on part of a name and a unique identifier"""
    slugify_name = slugify(name)[:5]
    random_id = str(uuid.uuid4())
    return f"{slugify_name}-{random_id}"


def generate_unique_slug_code(name, model):
    """Ensures that the generated slug is unique in the given model"""
    code = generate_slug(name)
    while model.objects.filter(code__exact=code).exists():
        code = generate_slug(name)
    return code


email_purpose = [("C", "Task Created"), ("F", "Task Finished")]
