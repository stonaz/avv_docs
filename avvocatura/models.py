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
    port = models.CharField(max_length=100,blank=True)
    service_type = models.CharField(max_length=100,blank=True)
    desc = models.CharField(max_length=100,blank=True)
    documentation_url = models.CharField(max_length=100,blank=True)
    svn = models.CharField(max_length=100,blank=True)
    deploy = models.CharField(max_length=100,blank=True)
    deps_to = CategoryField(blank=True)
    deps_by = CategoryField(blank=True)
    user = models.CharField(max_length=100,blank=True)
    start = models.CharField(max_length=100,blank=True)
    stop = models.CharField(max_length=100,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

