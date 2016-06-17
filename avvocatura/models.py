from django.db import models
from djangotoolbox.fields import ListField
from .forms import StringListField


class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
 
    
#class Server(models.Model):
#    name = models.CharField(max_length=100)
#    desc = models.CharField(max_length=100)
#    IP = models.TextField()
#    deps_down = CategoryField()
#    deps_up = CategoryField()
#    
#    class Meta:
#        ordering = ['name']
        
class Host(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    IP = models.TextField()
    deps_down = CategoryField()
    deps_up = CategoryField()
    services = CategoryField()
    
    class Meta:
        ordering = ['name']
        

class Service(models.Model):
    name = models.CharField(max_length=100)
    server = models.CharField(max_length=100)
    deps_by = CategoryField()
    port = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    deps_to = CategoryField()
    deps_by = CategoryField()
    so_user = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    stop = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']

