import pygraphviz as pgv
import time
import os
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required,user_passes_test
from ..models import Host,Service



def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        #print 'non trovato nel DB'
        return None

#def index(request):
#    host_list = Host.objects.all()
#    context = {'host_list': host_list}
#    return render(request, 'avvocatura/index.html', context)

@login_required
def spegnimento_doc(request):
    return render(request, 'avvocatura/spegnere.html')

@login_required
def accensione_doc(request):
    return render(request, 'avvocatura/accendere.html')

@login_required()
def serve_secure_static(request, file_root=os.path.join(settings.STATIC_ROOT, 'docs')):
    if not request.method == 'GET':
        return HttpResponseBadRequest('Only GET allowed')

    if not 'file' in request.GET:
        return HttpResponseBadRequest('File query must be provided')

    # make sire loggen user is allowed to see the file
    # maybe check some custom permission

    file_path = request.GET['file']
    #file_path = "docs/accendere.html"
    

    # if in DEBUG, make Django serve static file
    # because nginx might not be configured
    if settings.DEBUG:
        abs_file_path = os.path.join(file_root, file_path)
        file_data = open(abs_file_path, 'rb').read()
        return HttpResponse(file_data, mimetype=mimetypes.guess_type(file_path))

    # else make nginx serve static file
    else:
        redirect_url = '/docs/%s' % file_path
        response = HttpResponse()
        response['X-Accel-Redirect'] = redirect_url
        return response


