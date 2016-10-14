from django.core.exceptions import ObjectDoesNotExist
from ..models import Service

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        #print 'non trovato nel DB'
        return None

def dep_add(dep_kind,service,dep_list):
    for dep in dep_list:
        if len(dep) > 0: #non fare niente se nella lista ci sono strighe vuote
            linked_service = Service.objects.get(name=dep)
            print "Servizio a cui aggiungere la dipendenza: "
            print linked_service
            if dep_kind=='TO':
                existing_deps = linked_service.deps_by
                    #print type(existing_deps)
                if str(service) not in existing_deps:
                    existing_deps.append(str(service))
                linked_service.deps_by=existing_deps
                linked_service.save()
            if dep_kind=='BY':
                existing_deps = linked_service.deps_to
                    #print type(existing_deps)
                if str(service) not in existing_deps:
                    existing_deps.append(str(service))
                linked_service.deps_to=existing_deps
                linked_service.save()
                
def dep_delete(dep_kind,service,dep_list):
    for dep in dep_list:
        if len(dep) > 0: #non fare niente se nella lista ci sono strighe vuote
            linked_service = Service.objects.get(name=dep)
            print "Servizio da cui rimuovere la dipendenza: "
            print linked_service
            if dep_kind=='TO':
                existing_deps = linked_service.deps_by
                #print type(existing_deps)
                if str(service)  in existing_deps:
                    existing_deps.remove(str(service))
                linked_service.deps_by=existing_deps
                linked_service.save()
            if dep_kind=='BY':
                existing_deps = linked_service.deps_to
                #print type(existing_deps)
                if str(service)  in existing_deps:
                    existing_deps.remove(str(service))
                linked_service.deps_to=existing_deps
                linked_service.save()
                        
def dependencies_link(deps_before,service,deps_post,kind):
    print kind
    print deps_post
    test = len(deps_post[0])
    if (test < 1): # Nel form e' stata impostata nessuna dipendenza, rimuovi quelle che c'erano
            dep_delete(kind,service,deps_before)
    else: # Nel form sono state impostate dipendenze, aggiungile a quelle che c'erano
        if kind == "TO":
            deps_to_delete = [dep for dep in deps_before if dep not in service.deps_to]
            print 'Dip da eliminare'
            print deps_to_delete
            dep_delete(kind,service,deps_to_delete)
            dep_add(kind,service,service.deps_to)
        if kind == "BY":
            deps_to_delete = [dep for dep in deps_before if dep  not in service.deps_by]
            print 'Dip da eliminare'
            print deps_to_delete
            dep_delete(kind,service,deps_to_delete)
            dep_add(kind,service,service.deps_by)
            
def dependencies_link_add(service,deps_post,kind):
    if kind == "TO":
        dep_add(kind,service,service.deps_to)
    if kind == "BY":
        dep_add(kind,service,service.deps_by)