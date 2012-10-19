import settings
import sh
import os
from celery import task

@task
def run_repeatmasker(node):
    
    # check if output dir exists
    output_dir = '%s/%02.0d/' % (settings.REPEATMASKER_OUTPUT_DIR, node.pk)
    if os.path.exists(output_dir):
        # don't regenerate if it already exists
        #return output_dir
        return 'already gen'
        

    try:
        os.makedirs(output_dir)
    except:
        pass

    repeatmasker = sh.Command(settings.REPEATMASKER_EXEC)

    # generate source file
    input_file = '%s/input.fasta' % (output_dir)
    fp = open(input_file,'w')
    fp.write('>node-%02.0d\n%s\n' % (node.pk,node.sequence))
    fp.close()
                                                                                                                                                 
    repeatmasker(input_file,'-html','-dir', output_dir,'-species', 'drosophila')

    return 'started!'
    #ex command
    #repeatmasker../../repeatmaskertest/Fly_dm3.fasta -html -dir /home/rmcl/dnaseq/repeatmaskertest/fly2^C-species drosophila
    #return output_dir
