import settings
import sh



def run_repeatmasker(node):
    
    # check if output dir exists
    output_dir = '%s/%2.0d/' % (settings.REPEATMASKER_OUTPUT_DIR, node.pk)
    if os.path.exists(output_dir):
        # don't regenerate if it already exists
        return output_dir
        
    os.makedirs(output_dir)
    
    repeatmasker = sh.Command("/home/rmcl/dnaseq/repeatmaskertest")

    # generate source file
    input_file = '%s/input.fasta' % (input_dir)
    fp = open(input_file,'w')
    fp.write('>node-%2.0d\n%s\n' % (node.pk,node.sequence))
    fp.close()
                                                                                                                                                 
    repeatmasker('%s -html -dir %s -species drospila' % (input_file, output_dir))

    #ex command
    #repeatmasker../../repeatmaskertest/Fly_dm3.fasta -html -dir /home/rmcl/dnaseq/repeatmaskertest/fly2^C-species drosophila
    return output_dir
