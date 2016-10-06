import pygraphviz as pgv
import time
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse
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


