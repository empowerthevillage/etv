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
    
class type(models.Model):
    type        = models.CharField(max_length=270)

    objects     = VariationManager()

    def __str__(self):
        return self.type

class size(models.Model):
    size        = models.CharField(max_length=270)

    objects     = VariationManager()
    def __str__(self):
        return self.size

class weight(models.Model):
    weight      = models.CharField(max_length=270)

    def __str__(self):
        return self.weight

class color(models.Model):
    color   = models.CharField(max_length=270)
    objects     = VariationManager()
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

class ItemManager(models.Manager):
    
    def cart_filter(self, size, type, color):
        qs = self.get_queryset().filter(type=type).filter(color=color).filter(size=size)
        if qs.count() == 1:
            return qs.first()
        return None

class item(models.Model):
    size        = models.ForeignKey(size, on_delete=models.CASCADE)
    color       = models.ForeignKey(color, on_delete=models.CASCADE)
    type        = models.ForeignKey(type, on_delete=models.CASCADE, null=True, blank=True)
    inventory   = models.IntegerField(blank=True, null=True, default=0)

    objects     = ItemManager()

    def __str__(self):
        return '%s-%s-%s' %(self.size, self.color, self.type)

    def get_inventory(self, type):
        type_qs = self.objects.filter(type=type)
        available = type_qs.filter(self.inventory > 0)
        return available
    
    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"

class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured=True)
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    def active(self):
        return self.get_queryset().filter(active=True)
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(color__icontains=query)
        return self.get_queryset().filter(lookups, active=True).distinct()

class product(models.Model):
    title       = models.CharField(max_length=250)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    card_description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    type        = models.ForeignKey(type, null=True, blank=True, on_delete=models.CASCADE)
    colors        = models.ManyToManyField(color, blank=True)
    sizes       = models.ManyToManyField(size, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    shipping_weight = models.ManyToManyField(weight)
    sale_active = models.BooleanField(default=False)
    sale_price  = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True)
    images = models.ManyToManyField(image)
    variations   = models.ManyToManyField(item)

    objects     = ProductManager()

    def get_absolute_url(self):
        return reverse("merchandise:detail", kwargs={"slug":self.slug})
    
    def __str__(self):
        return str(self.title)

    @property
    def get_price(self):
        if self.sale_price and self.sale_active:
            return self.sale_price
        return self.price
    @property
    def get_html_price(self):
        price = self.get_price
        if price == self.sale_price:
            return "<p><span>%s</span> <span style='color:red;text-decoration:line-through;'>%s</span></p>" %(self.sale_price, self.price)
        else:
            return "<p>%s</p>" %(self.price)
    @property
    def get_images(self):
        return self.images.all()

    @property
    def get_variations(self):
        return self.variations.all()

    @property
    def get_colors(self):
        return self.colors.all()

    @property
    def get_sizes(self):
        return self.sizes.all()

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=product)

class inventory(models.Model):
    product     = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
    size        = models.ForeignKey(size, on_delete=models.CASCADE, null=True, blank=True)
    color       = models.ForeignKey(color, on_delete=models.CASCADE, null=True, blank=True)
    quantity    = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


