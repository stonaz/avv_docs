from django.contrib.admin import site, ModelAdmin
from models import Service,Host
 
def deps_by(instance):
    print type(instance.deps_by)
    #return ', '.join(str(instance.deps_by))
    return ','.join(str(d) for d in instance.deps_by)


 
class ServerAdmin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['deps_by'].widget.attrs['style'] = 'width: 45em;'
        return form
    list_display = ['name', deps_by]
 
site.register(Service, ServerAdmin)
site.register(Host, ModelAdmin)
