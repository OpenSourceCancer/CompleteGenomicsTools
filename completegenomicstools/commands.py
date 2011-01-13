from completegenomicstools.main import subparsers
from completegenomicstools.formats import DepthOfCoverageFile
import itertools
import csv

def prepcgh(args):
    tfile = DepthOfCoverageFile(args.tumorfile)
    nfile = DepthOfCoverageFile(args.normalfile)
    if(nfile.header['GENOME_REFERENCE']!=tfile.header['GENOME_REFERENCE']):
        raise Exception('Genome references not matching')
    windowsize=int(tfile.header['WINDOW_WIDTH'])/2
    
    for (tline,nline) in itertools.izip(tfile,nfile):
        if(args.format=='circos'):
            print "%s %d %d %f" % (tline[0].replace("chr","hs"),tline[1]-windowsize,tline[1]+windowsize,tline[5]/nline[5])
        else:
            print "%s\t%d\t%d\t%f" % (tline[0],tline[1]-windowsize,tline[1]+windowsize,tline[5]/nline[5])

prepcgh_parser = subparsers.add_parser('prepcgh',help="Prepare CGH files from tumor/normal pairs")
prepcgh_parser.add_argument("-t","--tumor-file",required=True,
                            dest="tumorfile",help="The name of a depthOfCoverage file from Complete Genomics associate with a tumor")
prepcgh_parser.add_argument("-n","--normal-file",required=True,
                            dest="normalfile",help="The name of a depthOfCoverage file from Complete Genomics associated with a paired normal")
prepcgh_parser.add_argument("-f","--format",default="circos",choices=['tdt','circos'],
                            dest="format",help="output format, tdt for tab-delimited text or circos for circos copy number file")
prepcgh_parser.set_defaults(func=prepcgh)


def junc2circos(args):
    f = csv.reader(open(args.junctionfile,'r'),delimiter="\t")
    line = f.next()
    while(len(line)==2):
        line=f.next()
    f.next()
    for line in f:
        print "%s %s %d %d\n%s %s %d %d" % (line[0],line[1].replace('chr','hs'),
                                                  int(line[2]),int(line[2])+int(line[4]),
                                                  line[0],line[5].replace('chr','hs'),
                                                  int(line[6]),int(line[6])+int(line[8]))


junc2circos_parser=subparsers.add_parser('junc2circos',help='Convert Complete Genomics junction files to circos')
junc2circos_parser.add_argument("junctionfile",help="Name of a complete genomics junction file (or junctiondiff file)")
junc2circos_parser.set_defaults(func=junc2circos)


        
    
    

