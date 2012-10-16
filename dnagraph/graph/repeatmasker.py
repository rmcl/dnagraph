import dnagraph.settings as settings
import sh
import os

def get_table(node):
    tbl_file= '%s/%02.0d/input.fasta.tbl' % (settings.REPEATMASKER_OUTPUT_DIR, node.pk)
    try:
        f = open(tbl_file)
        tbl = ''.join(f.readlines())
        f.close()
    except IOError:
        #run_repeatmasker(node)
        return 'Running repeatmasker. Refresh to view output.'

    return tbl

def run_repeatmasker(node):
    
    # check if output dir exists
    output_dir = '%s/%02.0d/' % (settings.REPEATMASKER_OUTPUT_DIR, node.pk)
    if os.path.exists(output_dir):
        # don't regenerate if it already exists
        #return output_dir
        pass

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
                                                                                                                                                 
    return  repeatmasker(input_file,'-html','-dir', output_dir,'-species', 'drosophila')

    
    #ex command
    #repeatmasker../../repeatmaskertest/Fly_dm3.fasta -html -dir /home/rmcl/dnaseq/repeatmaskertest/fly2^C-species drosophila
    #return output_dir
