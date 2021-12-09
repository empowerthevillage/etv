import random
from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from etv.utils import *
from django.db.models.signals import pre_save, post_save

class VariationManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    

class size(models.Model):
    size        = models.CharField(max_length=270)

    objects     = VariationManager()
    def __str__(self):
        return self.size


class color(models.Model):
    color   = models.CharField(max_length=270)

    def __str__(self):
        return self.color


class image(models.Model):
    image   = models.FileField()
    image_id      = models.CharField(max_length=50, null=True, blank=True, unique=True)
    default = models.BooleanField(default=False)
    order_by    = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['order_by',]

    def __str__(self):
        return str(self.image)

    def get_path(self):
        return 'https://d1z669787inm16.cloudfront.net/media/%s' %(self.image)

def pre_save_create_image_id(sender, instance, *args, **kwargs):
    if not instance.image_id:
        instance.image_id = unique_image_id_generator(instance)

pre_save.connect(pre_save_create_image_id, sender=image)


class Variation(models.Model):
    size = models.ForeignKey(size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(color, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s-%s' %(self.size, self.color)

class newProduct(models.Model):
    title       = models.CharField(max_length=250)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    card_description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    shipping_weight = models.IntegerField(null=True, blank=True)
    sale_active = models.BooleanField(default=False)
    sale_price  = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True)
    images = models.ManyToManyField(image)
    inventory   = models.ManyToManyField(Variation, through='newInventory')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['price']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    @property
    def get_images(self):
        return self.images.all()

    @property
    def get_colors(self):
        colors = set(self.inventory.select_related('color').distinct("color").all()) 
        return colors

    @property
    def get_sizes(self):
        sizes = set(self.inventory.select_related('size').distinct('size').all())
        return sizes

def newproduct_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(newproduct_pre_save_receiver, sender=newProduct)

def inventory_sku_generator(instance, new_sku=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_sku is not None:
        sku = new_sku
    else:
        sku = "{id}-{randstr}".format(
                    id=instance.product.id,
                    randstr=random_string_generator(size=4)
                )

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(sku=sku).exists()
    if qs_exists:
        new_sku = "{id}-{randstr}".format(
                    sku=sku,
                    randstr=random_string_generator(size=4)
                )
        return inventory_sku_generator(instance, new_sku=new_sku)
    return sku

class newInventory(models.Model):
    sku         = models.CharField(max_length=270, blank=True, null=True)
    product     = models.ForeignKey(newProduct, on_delete=models.CASCADE)
    variation   = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)

    def __str__(self):
        return self.sku

    class Meta:
        ordering = ['sku', 'quantity']
        verbose_name = 'SKU'
        verbose_name_plural = 'Inventory'

def inventory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.sku:
        instance.sku = inventory_sku_generator(instance)

pre_save.connect(inventory_pre_save_receiver, sender=newInventory)