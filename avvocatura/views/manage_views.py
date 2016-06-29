import pygraphviz as pgv
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from ..models import Host,Service
from django.contrib.auth.decorators import login_required


def host_add(request):
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    if request.POST:
        name=request.POST['name']
        ip=request.POST['ip']
        desc=request.POST['desc']
        services = request.POST.getlist('services')
        host=Host(name=name,services=services,IP=ip,desc=desc)
        host.save()
    context = {'services_list': services_list,'host_list': host_list}
    return render(request, 'avvocatura/add_host.html', context)

@login_required
def service_add(request):
    host_list = Host.objects.all()
    services_list = Service.objects.all()
    if request.POST:
        name=request.POST['name']
        port=request.POST['port']
        desc=request.POST['desc']
        documentation_url=request.POST['documentation_url']
        host = request.POST['host']
        service_type = request.POST['service_type']
        svn = request.POST['svn']
        deploy = request.POST['deploy']
        start = request.POST['start']
        stop = request.POST['stop']
        user = request.POST['user']
        deps_to = request.POST.getlist('deps_to')
        deps_by = request.POST.getlist('deps_by')
        service=Service(name=name,port=port,server=host,desc=desc,service_type=service_type,deps_to=deps_to,deps_by=deps_by,svn=svn,user=user,start=start,stop=stop,documentation_url=documentation_url,deploy=deploy )
        service.save()
    context = {'services_list': services_list,'host_list': host_list}
    return render(request, 'avvocatura/add_service.html', context)

@login_required
def host_update(request,id):
    host = Host.objects.get(id=id)
    message=""
    if request.POST:
        host.name=request.POST['name']
        host.IP=request.POST['ip']
        host.desc=request.POST['desc']
        host.services = request.POST.getlist('services')
        #host=Host(name=name,services=services,IP=ip,desc=desc)
        host.save()
        message="Host modificato"
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    
    print host.services
    host_services_list=[]
    for service in services_list:
        host_service = {}
        host_service['name'] = service.name
        if service and service.name in host.services:
            print "found"
            host_service['selected'] = 1
        else:
            host_service['selected'] = 0
        host_services_list.append(host_service)
           
    print host_services_list       
    context = {'host_services_list': host_services_list,'services_list': services_list,'host_list': host_list,'host_selected':host,'message':message}
    print message
    return render(request, 'avvocatura/update_host.html', context)

@login_required
def service_update(request,id):
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    return HttpResponse('not implemented yet')

@login_required
def manage_index(request):
    context = {}
    #services_list = Service.objects.all()
    #host_list = Host.objects.all()
    return render(request, 'avvocatura/manage_index.html', context)

#def get_or_none(classmodel, **kwargs):
#    try:
#        return classmodel.objects.get(**kwargs)
#    except classmodel.DoesNotExist:
#        #print 'non trovato nel DB'
#        return None
#
#def index(request):
#    host_list = Host.objects.all()
#    context = {'host_list': host_list}
#    return render(request, 'avvocatura/index.html', context)
#
#def hosts_index(request):
#    host_list = Host.objects.all()
#    context = {'host_list': host_list}
#    return render(request, 'avvocatura/hosts_index.html', context)
#
#def servizi_index(request):
#    services_list = Service.objects.all()
#    context = {'services_list': services_list}
#    return render(request, 'avvocatura/services_index.html', context)
#
#def drawDeps(deps_list,dep,node,graph):
#    #print "Trovata dipendenza:" + dep
#    
#        
#    dep_object=get_or_none(Service,name=dep)
#    if dep_object is not None:
#        dep_name=dep_object.name
#        dep_subdeps=dep_object.deps_to
#        #print dep_name
#        #print dep_subdeps
#        graph.add_edge(node,dep_name)
#        #print "Aggiunta relazione da " + node + " a " + dep_name
#        if dep not in deps_list:
#            #print "Dipendenza ancora da trattare"
#            DrawSubDeps(deps_list,dep_subdeps,dep,graph)
#    else:
#        graph.add_edge(node,dep)
#    deps_list.append(dep)
#        #print "Aggiunta relazione da " + node +  " a " + dep
#        #DrawSubDeps(dep_subdeps,dep,graph)
#    
#    
#def DrawSubDeps(deps_list,subdeps,node,graph):
#    for subdep in subdeps:
#        #print "Sottodipendenze di %s", node
#        drawDeps(deps_list,subdep,node,graph)
#        
#def DrawDepsUp(dep,node,graph):
#    graph.add_node(dep,shape='box',style='filled',color="gray") # adds node 'a'
#    graph.add_edge(dep,node)
#    e=graph.get_node(node)
#    e.attr['color']='green'
#
#
#def host_detail(request,id):
#    host_list = Host.objects.all()
#    host = Host.objects.get(id=id)  
#    node = host.name
#    services = host.services
#    service_list=[]
#    for service in services:
#        s={}
#        s['name']=service
#        
#        service_details = get_or_none(Service,name=service)
#        if service_details is not None:
#            s['id']=service_details.id
#        else:
#            s['id']="not present"
#        service_list.append(s)
#    print service_list
#    context = {'host_list': host_list,'server' : host, 'service_list':service_list}  
#    return render(request, 'avvocatura/show_host.html', context)
#
#
#def service_detail(request,id):
#    service_list = Service.objects.all()
#    service = Service.objects.get(id=id)
#    deps_list= []
#    node = service.name
#    deps_down = service.deps_to
#    deps_up = service.deps_by
#    server = service.server
#    print server
#    host_list=[]
#    for host in server:
#        print host
#        h={}
#        h['name']=host
#        
#        host_details = get_or_none(Host,name=host)
#        if host_details is not None:
#            h['id']=host_details.id
#        else:
#            h['id']="not present"
#            print h
#        host_list.append(h)
#    
#    filename = 'avvocatura/static/avvocatura/' + node + '_deps_down.png'
#    context_filename = 'avvocatura/' + node + '_deps_down.png'
#    filename2 = 'avvocatura/static/avvocatura/' + node + '_deps_up.png'
#    context_filename2 = 'avvocatura/' + node + '_deps_up.png'
#
#    if settings.DEBUG == False :
#        filename = settings.STATIC_ROOT + 'avvocatura/'+ node + '_deps_down.png'
#        filename2 = settings.STATIC_ROOT + 'avvocatura/'+ node + '_deps_up.png'
#
#    G=pgv.AGraph(strict=False,directed=True)
#    G.add_node(node,shape='box',style='filled',color="green") # adds node 'a'
#    for dep in deps_down:
#        #print "LIST:"
#        #print deps_list
#        drawDeps(deps_list,dep,node,G)
#        
#    G.layout(prog='dot')    
#    G.draw(filename)
#    
#    G2=pgv.AGraph(strict=False,directed=True)
#    for dep in deps_up:
#        DrawDepsUp(dep,node,G2)
#    G2.layout(prog='dot')    
#    G2.draw(filename2)
#    
#    context = {'service_list': service_list,'filename':context_filename, 'filename2':context_filename2,'service' : service, 'host_list':host_list}  
#    return render(request, 'avvocatura/show_service.html', context)
