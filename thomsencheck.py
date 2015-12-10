#!/usr/bin/env python

#import BeautifulSoup
import Levenshtein
import codecs
import argparse
import sys
import os
import gzip

parser = argparse.ArgumentParser(description='check if a line appears in a file, fuzzy by Levenshtein distance (all lowercase comparison)')
parser.add_argument(metavar='L', type=str, nargs='*', dest='line', default=None,
                   help='line to look for, if empty use stdin')
parser.add_argument('-d', '--distance', type=int, dest='distance', default=4,
                   help='max Levenshtein distance')
parser.add_argument('-f', '--file', action='append', default=[os.path.join(os.path.dirname(__file__),'journallist_thomsen.txt.gz'), os.path.join(os.path.dirname(__file__),'journallist_thum.txt')], dest='file',
                   help='files to be processed, gzipped files are handled')

args = parser.parse_args()
#print args

tlists={}
for filename in args.file:
    print "--- reading "+filename+" ---"
    try:
        fbase, fext = os.path.splitext(filename)
        if fext.lower() == '.gz':
            with gzip.open(filename) as f:
                #cgr=codecs.getreader('zlib')
                fd = codecs.getreader("utf-8")(f)
                tlists[filename] = fd.readlines()
        else:
            with codecs.open(filename, "r", "utf8") as f:
                tlists[filename]=f.readlines()
    except: # Error as e:
        print "error with "+filename
        continue

for bbs in args.line:
    for f,goodlist in tlists.items():
        for g in goodlist:
            b=bbs.decode(sys.stdin.encoding)
            if Levenshtein.distance(g.lower().strip(),unicode(b).lower().strip()) < args.distance:
                print "%s similar to %s in %s" % (g, b,f)

if len(args.line) == 0:
    while True:
        bbs = sys.stdin.readline()
        if not bbs:
            break
        for f,goodlist in tlists.items():
            for g in goodlist:
                b=bbs.decode(sys.stdin.encoding)
                if Levenshtein.distance(g.lower().strip(),unicode(b).lower().strip()) < args.distance:
                    print "%s similar to %s in %s" % (g, b,f)
