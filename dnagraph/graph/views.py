from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import repeatmasker
import graph.models as graph_models


def _get_first_child_sequence(sequence, children, start_offset = 0):
    earliest_start_pos = len(sequence)
    earliest_child = None
    for c in children:
        start_pos = sequence.find(c.sequence, start_offset)
        #if start_pos < 0:
        #    print 'not found'
        #    continue
        if start_pos < earliest_start_pos:
            earliest_child = c
            earliest_start_pos = start_pos
    
    if earliest_child is None:
        raise Exception('Could not find anymore children')
    
    return earliest_start_pos, earliest_child

def exec_repeatmasker(request, node_id):
    node = graph_models.Node.objects.get(pk = node_id)
    
    repeatmasker.run_repeatmasker_if_not_already_queued(node)
    return HttpResponse( 'queued repeat masker if not already queued.')


def show(request, node_id ):
    
    # number of nucleotides per line
    #col_wrap = request.GET.get('wrap', 80)
    
    n = graph_models.Node.objects.get(pk = node_id)
    
    # Get all nodes which are children of this node
    children = graph_models.Node.objects.filter(parents__in=[n.pk])

    children_set = set(children.all())

    children_ordered = []

    subseq_pos = []
    start_pos = 0
    while len(children_set) > 0:
        start_pos, child = _get_first_child_sequence(n.sequence, children_set, start_pos)
        end_pos = start_pos + len(child.sequence)
        
        print 'END POS',start_pos, end_pos
        
        subseq_pos.append((start_pos,end_pos, child))
        
        start_pos = end_pos
        children_set.remove(child)
        children_ordered.append(child)
        
        print child.pk, child.locations
        
        
    annotated_seq = ''
    bla = ''

    if len(subseq_pos) > 0:

        cur_pos = 0
        for subseq_index in range(len(subseq_pos)):
            subseq = subseq_pos[subseq_index]
            if cur_pos - subseq[0] > 0:
                annotated_seq += n.sequence[cur_pos:subseq[0]]
                bla += n.sequence[cur_pos:subseq[0]]
                cur_pos = subseq[0]
            
            annotated_seq += '<a name="seq' + str(subseq[2].pk) + '"></a><span class="seq' + str(subseq_index) + ' seqid'+ str(subseq[2].pk) +'">' + n.sequence[subseq[0]:subseq[1]] + "</span>"
            bla += n.sequence[subseq[0]:subseq[1]]
            cur_pos = subseq[1]
    
     
        if subseq_pos[-1][1] != len(n.sequence):
            annotated_seq += n.sequence[subseq_pos[-1][1]:]
            bla += n.sequence[subseq_pos[-1][1]:]
    else:
        # no children so just display whole thing
        annotated_seq = n.sequence
    
    
    repeatmasker_tbl = repeatmasker.get_table(n)
    repeatmaskedseq = repeatmasker.get_masked(n)
    
    return render_to_response('graph/show.html', {
        'node': n,
        'annotated_seq': annotated_seq,
        'children': children_ordered,
        'parents': n.parents.all(),
        'repeatmasker_tbl': repeatmasker_tbl,
        'repeatmaskedseq': repeatmaskedseq,
    }, context_instance=RequestContext(request))
