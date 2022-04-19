from re import T
import django
from django.db import models

class dashboardModelManager(models.Manager):
   
    def dash_register(self, model):
        (registration, created) = dashboardModel.objects.get_or_create(model_name=str(model.__name__))
        registration.app_name = model._meta.app_label
        registration.category = model.objects.dashboard_category()
        registration.save()
        return registration
        
        #if dashboardModel.objects.filter(model_name=str(model.__name__).lower()).first() is not None:
        #    registration = dashboardModel.objects.filter(model_name=str(model.__name__).lower()).first()
        #    registration.model_name = str(model.__name__).lower()
        #    registration.model_name_verbose = model._meta.verbose_name
         #   registration.model_name_plural = model._meta.verbose_name_plural
         #   registration.app_name = model._meta.app_label
          #  registration.display_qty = model.objects.dashboard_display_qty()
          #  registration.category = model.objects.dashboard_category()
          #  registration.list_fields_JSON = model.objects.dashboard_get_fields()
          #  registration.view_fields = model.objects.dashboard_get_view_fields()
          #  try:
          #      registration.grouping = model.objects.get_grouping()
          #  except:
          #      pass
          #  registration.save()

          #  return registration

        #else:
         #   registration = dashboardModel()
          #  registration.model_name = str(model.__name__).lower()
           # registration.model_name_verbose = model._meta.verbose_name
            #registration.model_name_plural = model._meta.verbose_name_plural
            #registration.app_name = model._meta.app_label
            #registration.display_qty = model.objects.dashboard_display_qty()
            #registration.category = model.objects.dashboard_category()
            #registration.list_fields_JSON = model.objects.dashboard_get_fields()
            #registration.view_fields = model.objects.dashboard_get_view_fields()
            #try:
            #    registration.grouping = model.objects.get_grouping()
            #except:
            #    pass
            #registration.save()

            #return registration

class dashboardModel(models.Model):
    model_name          = models.CharField(max_length=200)
    model_name_plural   = models.CharField(max_length=200)
    model_name_verbose  = models.CharField(max_length=50, null=True, blank=True)
    model_name_verbose_plural = models.CharField(max_length=50, null=True, blank=True)
    category            = models.CharField(max_length=50, null=True, blank=True)
    grouping            = models.CharField(max_length=100, null=True, blank=True)
    app_name            = models.CharField(max_length=200)
    list_fields         = models.CharField(max_length=200, null=True, blank=True)
    list_fields_JSON    = models.JSONField(null=True, blank=True)
    list_display        = models.CharField(max_length=500, null=True, blank=True)
    list_filter         = models.CharField(max_length=500, null=True, blank=True)
    view_fields         = models.JSONField(null=True, blank=True)
    edit_fields         = models.CharField(max_length=1000, null=True, blank=True)
    search_fields       = models.CharField(max_length=500, null=True, blank=True)
    ordering            = models.CharField(max_length=500, null=True, blank=True)
    display_qty         = models.IntegerField(null=True, blank=True)

    objects = dashboardModelManager()

    def __str__(self):
        return self.model_name

    @property
    def get_model_name(self):
        model = django.apps.apps.get_model(str(self.app_name), str(self.model_name))
        return model._meta.verbose_name

    @property
    def get_model_name_plural(self):
        model = django.apps.apps.get_model(str(self.app_name), str(self.model_name))
        return model._meta.verbose_name_plural
    
    @property
    def get_grouping(self):
        model = django.apps.apps.get_model(str(self.app_name), str(self.model_name))
        return model.objects.get_grouping()