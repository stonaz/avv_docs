import pygraphviz as pgv
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from models import Server


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        print 'non trovato nel DB'
        return None

def index(request):
    host_list = Server.objects.all()
    context = {'host_list': host_list}
    return render(request, 'avvocatura/index.html', context)

def drawDeps(dep,node,graph):
    print "Trovata dipendenza:" + dep
    dep_object=get_or_none(Server,name=dep)
    if dep_object is not None:
        dep_name=dep_object.name
        dep_subdeps=dep_object.deps_down
        print dep_name
        print dep_subdeps
        graph.add_edge(node,dep_name)
        print "Aggiunta relazione da " + node + "a " + dep_name
        DrawSubDeps(dep_subdeps,dep,graph)
        
def DrawSubDeps(subdeps,node,graph):
    for subdep in subdeps:
        drawDeps(subdep,node,graph)
        
def DrawDepsUp(dep,node,graph):
    graph.add_node(dep,shape='box',style='filled',color="gray") # adds node 'a'
    graph.add_edge(dep,node)
    e=graph.get_node(node)
    e.attr['color']='green'


def detail(request,id):
    host_list = Server.objects.all()
    server = Server.objects.get(id=id)
    
    node = server.name
    deps_down = server.deps_down
    deps_up = server.deps_up

    print type(deps_down)
    desc = server.desc
    filename = 'avvocatura/static/avvocatura/' + node + '_deps_down.png'
    context_filename = 'avvocatura/' + node + '_deps_down.png'
    filename2 = 'avvocatura/static/avvocatura/' + node + '_deps_up.png'
    context_filename2 = 'avvocatura/' + node + '_deps_up.png'

    #print settings.STATIC_ROOT
    if settings.DEBUG == False :
        filename = settings.STATIC_ROOT + 'avvocatura/'+ node + '_deps_down.png'
        filename2 = settings.STATIC_ROOT + 'avvocatura/'+ node + '_deps_up.png'
    #print filename

    G=pgv.AGraph(strict=False,directed=True)
    G.add_node(node,shape='box',style='filled',color="green") # adds node 'a'
    for dep in deps_down:
        #print type(dep)
        drawDeps(dep,node,G)
        #G.add_edge(node,dep)
        #print type(dep)
        #if type(dep) is dict:
        #    print 'subdep found'
        #    for dep,subdeps in dep.iteritems():
        #        for subdep in subdeps:
        #            print type(subdep)
        #            G.add_edge(dep,subdep)
        #G.add_edge(node,dep)
    G.layout(prog='dot')    
    G.draw(filename)
    
    G2=pgv.AGraph(strict=False,directed=True)
    for dep in deps_up:
        DrawDepsUp(dep,node,G2)
    G2.layout(prog='dot')    
    G2.draw(filename2)
    
    context = {'host_list': host_list,'filename':context_filename, 'filename2':context_filename2,'server' : server}  
    return render(request, 'avvocatura/showpng.html', context)
