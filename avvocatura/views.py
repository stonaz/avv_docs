import pygraphviz as pgv
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from models import Server


def index(request):
    host_list = Server.objects.all()
    context = {'host_list': host_list}
    return render(request, 'avvocatura/index.html', context)

def drawDeps(dep,node,graph):
    if type(dep) is unicode:
        graph.add_edge(node,dep)
        print dep
    if type(dep) is dict:
        print 'subdep found:' 
        DrawSubDeps(dep,node,graph)
        
def DrawSubDeps(dep,node,graph):
    for dep,subdeps in dep.iteritems():
        graph.add_edge(node,dep)
        for subdep in subdeps:
            drawDeps(subdep,dep,graph)
            print type(subdep)
            
        #graph.add_edge(dep,subdep)

def detail(request,id):
    host_list = Server.objects.all()
    server = Server.objects.get(id=id)
    
    node = server.name
    deps = server.deps
    desc = server.desc
    filename = 'avvocatura/static/avvocatura/' + node + '.png'
    context_filename = 'avvocatura/' + node + '.png'
    #print settings.STATIC_ROOT
    if settings.DEBUG == False :
        filename = settings.STATIC_ROOT + 'avvocatura/'+ node + '.png'
    #print filename

    G=pgv.AGraph(strict=False,directed=True)
    G.add_node(node,shape='box',style='filled',color=".7 .3 1.0") # adds node 'a'
    for dep in deps:
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
    #G.write("postgres.dot")
    context = {'host_list': host_list,'filename':context_filename, 'server' : server}
    return render(request, 'avvocatura/showpng.html', context)
