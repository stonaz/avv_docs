from django.db import models
from djangotoolbox.fields import ListField
from .forms import StringListField


class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
 
    
class Server(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    IP = models.TextField()
    deps = CategoryField()
