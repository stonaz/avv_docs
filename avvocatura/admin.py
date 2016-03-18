from django.contrib.admin import site, ModelAdmin
from models import Service
 
def deps(instance):
    print type(instance.deps)
    #return ', '.join(str(instance.deps))
    return ','.join(str(d) for d in instance.deps)


 
class ServerAdmin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['deps'].widget.attrs['style'] = 'width: 45em;'
        return form
    list_display = ['name', deps]
 
site.register(Service, ServerAdmin)
