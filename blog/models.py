from django.db import models
from djangotoolbox.fields import ListField
from .forms import StringListField


class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
 
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    categories = CategoryField()
    comments = CategoryField()
    tags = CategoryField()