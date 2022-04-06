import django
from django.db import models

class dashboardModelManager(models.Manager):
   
    def dash_register(self, model):
        if dashboardModel.objects.filter(model_name=str(model._meta.verbose_name)).first() is not None:
            registration = dashboardModel.objects.filter(model_name=str(model._meta.verbose_name)).first()
            registration.model_name = model._meta.verbose_name
            registration.model_name_plural = model._meta.verbose_name_plural
            registration.app_name = model._meta.app_label
            registration.list_fields_JSON = model.objects.dashboard_get_fields()
            registration.save()
            print('exists')
            return registration
        else:
            registration = dashboardModel()
            registration.model_name = model._meta.verbose_name
            registration.model_name_plural = model._meta.verbose_name_plural
            registration.app_name = model._meta.app_label
            registration.list_fields_JSON = model.objects.dashboard_get_fields()
            registration.save()
            print('new')
            return registration

class dashboardModel(models.Model):
    model_name          = models.CharField(max_length=200)
    model_name_plural   = models.CharField(max_length=200)
    app_name            = models.CharField(max_length=200)
    list_fields         = models.CharField(max_length=200, null=True, blank=True)
    list_fields_JSON         = models.JSONField(null=True, blank=True)
    list_display        = models.CharField(max_length=500, null=True, blank=True)
    list_filter         = models.CharField(max_length=500, null=True, blank=True)
    search_fields       = models.CharField(max_length=500, null=True, blank=True)
    ordering            = models.CharField(max_length=500, null=True, blank=True)
    display_qty         = models.IntegerField(null=True, blank=True)

    objects = dashboardModelManager()

    def __str__(self):
        return self.model_name

    @property
    def get_model_item(self):
        model = django.apps.apps.get_model(str(self.app_name), str(self.model_name))
        return model
    
