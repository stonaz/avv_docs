from django.db import models
from djangotoolbox.fields import ListField
from .forms import StringListField


class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
        
class Host(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    IP = models.TextField()
    services = CategoryField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class Service(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    documentation_url = models.CharField(max_length=100)
    svn = models.CharField(max_length=100)
    deploy = models.CharField(max_length=100)
    deps_to = CategoryField()
    deps_by = CategoryField()
    user = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    stop = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

