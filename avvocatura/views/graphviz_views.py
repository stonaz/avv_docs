import pygraphviz as pgv
import time
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required,user_passes_test
from ..models import Host,Service
from utils import *


@login_required
def index(request):
    host_list = Host.objects.all()
    context = {'host_list': host_list}
    return render(request, 'avvocatura/index.html', context)

@login_required
def hosts_index(request):
    host_list = Host.objects.all()
    menu_id='hosts'
    context = {'host_list': host_list,'menu': menu_id}
    
    return render(request, 'avvocatura/hosts_index.html', context)

@login_required
def servizi_index(request):
    services_list = Service.objects.all()
    menu_id='services'
    context = {'services_list': services_list,'menu': menu_id}
    return render(request, 'avvocatura/services_index.html', context)

def drawDeps(deps_list,dep,node,graph,node_shape):
    #print "Trovata dipendenza:" + dep
    if len(node) >=  1:
        graph.add_node(node,shape=node_shape) # adds node 'a'
        e = graph.get_node(node)
        if node_shape == "box":
            e.attr['color']='green'
            e.attr['style']='filled'
    dep_object=get_or_none(Service,name=dep)
    if dep_object is not None:
        dep_name=dep_object.name
        dep_subdeps=dep_object.deps_to
        #print dep_name
        #print dep_subdeps
        graph.add_edge(dep_name,node)
        #print "Aggiunta relazione da " + node + " a " + dep_name
        if dep not in deps_list:
            #print "Dipendenza ancora da trattare"
            DrawSubDeps(deps_list,dep_subdeps,dep,graph)
    else:
        graph.add_edge(dep,node)
    deps_list.append(dep)
        #print "Aggiunta relazione da " + node +  " a " + dep
        #DrawSubDeps(dep_subdeps,dep,graph)
    
    
def DrawSubDeps(deps_list,subdeps,node,graph):
    for subdep in subdeps:
        #print "Sottodipendenze di %s", node
        drawDeps(deps_list,subdep,node,graph,'ellipse')
        
def DrawDepsUp(dep,node,graph):
    graph.add_node(dep) # adds node 'a'
    graph.add_edge(node,dep)
    e=graph.get_node(node)
    e.attr['color']='green'
    e.attr['shape']='box'
    e.attr['style']='filled'

@login_required
def host_detail(request,id):
    host_list = Host.objects.all()
    host = Host.objects.get(id=id)  
    node = host.name
    services = host.services
    service_list=[]
    for service in services:
        s={}
        s['name']=service
        
        service_details = get_or_none(Service,name=service)
        if service_details is not None:
            s['id']=service_details.id
        else:
            s['id']="not present"
        service_list.append(s)
    menu_id='hosts'
    context = {'host_list': host_list,'server' : host, 'service_list':service_list,'menu': menu_id}  
    return render(request, 'avvocatura/show_host.html', context)

@login_required
def service_detail(request,id):
    service_list = Service.objects.all()
    service = Service.objects.get(id=id)
    deps_list= []
    node = service.name
    deps_down = service.deps_to
    deps_up = service.deps_by
    host = service.host
    host_details = get_or_none(Host,name=host)
    h={}
    h['name']=host
    if host_details is not None:
        h['id']=host_details.id
    else:
        h['id']="not present"
    print h
    
    ts = str(time.time())
    
    filename = 'avvocatura/static/avvocatura/graphics/' + node + '_deps_down.png'
    context_filename = 'avvocatura/graphics/' + node + '_deps_down.png?dummy=' + ts
    
    filename2 = 'avvocatura/static/avvocatura/graphics/' + node + '_deps_up.png'
    context_filename2 = 'avvocatura/graphics/' + node + '_deps_up.png?dummy=' + ts

    if settings.DEBUG == False :
        filename = settings.STATIC_ROOT + 'avvocatura/graphics/'+ node + '_deps_down.png'
        filename2 = settings.STATIC_ROOT + 'avvocatura/graphics/'+ node + '_deps_up.png'

    G=pgv.AGraph(strict=False,directed=True)
    G.graph_attr.update(size="8,8")
    for dep in deps_down:
        #print "LIST:"
        #print deps_list
        if len(dep) >=  1:
            drawDeps(deps_list,dep,node,G,'box')
        
    G.layout(prog='dot')
    
    G.draw(filename)
    
    
    G2=pgv.AGraph(strict=False,directed=True)
    G2.graph_attr.update(size="8,8")
    for dep in deps_up:
        print 'dep' + dep
        if len(dep) >=  1:
            DrawDepsUp(dep,node,G2)
    G2.layout(prog='dot')    
    G2.draw(filename2)
    menu_id='services'
    context = {'service_list': service_list,'filename':context_filename, 'filename2':context_filename2,'service' : service, 'host':h,'menu': menu_id}  
    return render(request, 'avvocatura/show_service.html', context)
