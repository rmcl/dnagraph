import settings
import sh
import os
import graph.tasks as graph_tasks

def get_table(node):
    tbl_file= '%s/%02.0d/input.fasta.tbl' % (settings.REPEATMASKER_OUTPUT_DIR, node.pk)
    try:
        f = open(tbl_file)
        tbl = ''.join(f.readlines())
        f.close()
    except IOError:
        run_repeatmasker_if_not_already_queued(node)
        return 'Running repeatmasker. Refresh to view output.'

    return tbl

def get_masked(node):
    tbl_file= '%s/%02.0d/input.fasta.masked' % (settings.REPEATMASKER_OUTPUT_DIR, node.pk)
    try:
        f = open(tbl_file)
        # first line is fasta label
        tbl = ''.join(f.readlines()[1:]).replace('\n','')
        f.close()
    except IOError:
        run_repeatmasker_if_not_already_queued(node)
        return 'None'

    return tbl

def run_repeatmasker_if_not_already_queued(node):
    if node.ran_repeatmasker != 1:
        graph_tasks.run_repeatmasker.delay(node)
        node.ran_repeatmasker = 1
        node.save()
