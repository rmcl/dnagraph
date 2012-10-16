import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnagraph.settings")
import sys
from django.core.management import setup_environ
from dnagraph import settings
import graph.models as graph_models

def parse_line(line):
    l = line.strip().split('\t')
    hits = l[2].split(',')
    hits = filter(lambda x: x!='', hits)
    
    parent_nodes = map(int, filter(lambda x: x !='', l[3].split(',')))
    index, length = map(int, (l[0],l[1]))
    
    #index = get_index(index)
    #parent_nodes = map(get_index, parent_nodes)
    
    return (index,length,parent_nodes, hits, l[4])

#def get_index(file_index):
#    '''Primary key in db starts at 1 not zero'''
#    return file_index + 1

if __name__ == "__main__":

    setup_environ(settings)
    


    f = open('../src_graphs/Fly_dm3_27_longest_graph.out','r')

    a = map(parse_line, f)
    i = 0
    stop = 5000
    for node in a:
        index, length, parent_nodes, hits, seq = node
        h = ','.join(hits)            
        
        n = graph_models.Node.objects.get_or_create(pk=index, length=length, locations=h, sequence=seq)
    
        if (i % 1000) == 0:
            print i
            
        i += 1
        
        if i > stop:
            break
    
    i = 0
    for node in a:
        index, length, parent_nodes, hits, seq = node

        n = graph_models.Node.objects.get(pk=index)
        
        for pn in parent_nodes:
            try:
                if pn == 0:
                    continue
                    
                parent = graph_models.Node.objects.get(pk=pn)
                n.parents.add(parent)
            except:
                print 'does not exist', pn
                pass
            
            if i > stop:
                break