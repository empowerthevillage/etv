from storages.backends.s3boto3 import S3Boto3Storage
import random
import string
from django.utils.text import slugify
from django.http import HttpResponse
from django.template.loader import get_template

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media')

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_subscription_id_generator(instance):
    braintree_id = random_string_generator(size=7)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(braintree_id=braintree_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return braintree_id

def unique_order_key_generator(instance):
    """
    This is for a Django product with a key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    """
    This is for a Django product with an order_id field
    """
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id

def unique_image_id_generator(instance):
    """
    This is for a Django product with an order_id field
    """
    image_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(image_id=image_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return image_new_id

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug