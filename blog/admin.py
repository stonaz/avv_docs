from django.contrib.admin import site, ModelAdmin
from models import Post
 
def categories(instance):
    return ', '.join(instance.categories)
 
class PostAdmin(ModelAdmin):
    list_display = ['title', categories]
 
site.register(Post, PostAdmin)
