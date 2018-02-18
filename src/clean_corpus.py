import sys
import os
from time import time
sys.path.insert(0, 'utils')
from preprocessing import clean_sentence

def main(root_dir, f_out, f_in):
    """
    Clean a whole corpus file and write cleaned sentences line by line into the output file.
    f_in: input (raw corpus) file path
    f_out: output (cleaned corpus) file path
    """
    f_in = os.path.join(root_dir, f_in)
    f_out = os.path.join(root_dir, f_out)

    start = time()
    print "Starting clean corpus..."
    with open(f_in, 'r') as raw_file:
        cleaned_file = open(f_out, 'w')
        for i, line in enumerate(raw_file):
            if i % 50000 == 0 and i > 0:
                print "%d sentences done..." % i
            cleaned_l = clean_sentence(line)
            if len(cleaned_l) > 0:
                cleaned_file.write("%s\n" % cleaned_l.encode('utf-8'))
        raw_file.close()
        cleaned_file.close()
    print "Corpus clean done in %0.3fs." % (time() - start)

main(sys.argv[1], sys.argv[2], sys.argv[3])