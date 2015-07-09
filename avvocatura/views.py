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

def detail(request,id):
    host_list = Server.objects.all()
    #client = MongoClient()
    #db = client.test
    #collection = db.avvocatura
    server = Server.objects.get(id=id)
    
    print server
    node = server.name
    deps = server.deps
    desc = server.desc
    filename = 'avvocatura/static/avvocatura/' + node + '.png'
    context_filename = 'avvocatura/' + node + '.png'
    print desc
    #print settings.STATIC_ROOT
    #if settings.DEBUG == False :
    #    filename = settings.STATIC_ROOT + 'avvocatura/'+ server['hostname'] + '.png'
    print filename
    

    #for server in collection.find():
    #    print server

    G=pgv.AGraph(strict=False,directed=True)
    G.add_node(node,shape='box',style='filled',color=".7 .3 1.0") # adds node 'a'
    for dep in deps:
        print type(dep)
        if type(dep) is dict:
            print 'subdep found'
            for dep,subdeps in dep.iteritems():
                for subdep in subdeps:
                    print type(subdep)
                    G.add_edge(dep,subdep)
        #print dep[1]
        G.add_edge(node,dep)
    G.layout(prog='dot')    
    G.draw(filename)
    G.write("postgres.dot")
    context = {'host_list': host_list,'filename':context_filename, 'server' : server}
    return render(request, 'avvocatura/showpng.html', context)
