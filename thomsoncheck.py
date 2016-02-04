#!/usr/bin/env python

#import BeautifulSoup
import Levenshtein
import codecs
import argparse
import sys
import os
import gzip
import re

defaultfiles=[]
defaultfiles.append(os.path.join(os.path.dirname(__file__),'journallist_thomson.txt.gz'))
defaultfiles.append(os.path.join(os.path.dirname(__file__),'journallist_thum.txt'))


parser = argparse.ArgumentParser(description='check if a line appears in a file, fuzzy by Levenshtein distance (all lowercase comparison)')
parser.add_argument(metavar='L', type=str, nargs='*', dest='line', default=None,
                   help='line to look for, if empty use stdin')
parser.add_argument('-d', '--distance', type=int, dest='distance', default=4,
                   help='max Levenshtein distance')
parser.add_argument('-r', '--regex', action="store_true", dest='regex',
                   help='use input lines as regex')
parser.add_argument('-f', '--file', action='append', dest='file',
                   help='files to be processed, gzipped files are handled. If not given, defaults to '+str(defaultfiles))

args = parser.parse_args()
#print args
if args.file is None:
    args.file=defaultfiles

tlists={}
for filename in args.file:
    print "--- reading "+filename+" ---"
    try:
        fbase, fext = os.path.splitext(filename)
        if fext.lower() == '.gz':
            with gzip.open(filename) as f:
                #cgr=codecs.getreader('zlib')
                fd = codecs.getreader("utf-8")(f)
                tlists[filename] = fd.read().splitlines()
        else:
            with codecs.open(filename, "r", "utf8") as f:
                tlists[filename]=f.read().splitlines()
    except: # Error as e:
        print "error with "+filename
        continue

def yieldlistorstdin(alist=[]):
    if len(alist)==0:
        while True:
            x=sys.stdin.readline()
            if not x:
                break
            if (len(x) < 2) or (x is None):
                continue
            yield x.strip()
    else:
        for x in alist:
            yield x

for bbs in yieldlistorstdin(args.line):
    if args.regex:
        rx=re.compile('.*'+bbs+'.*', flags=re.IGNORECASE)
    for f,goodlist in tlists.items():
        for g in goodlist:
            b=bbs.decode(sys.stdin.encoding if sys.stdin.encoding else 'UTF-8')
            if Levenshtein.distance(g.lower().strip(),unicode(b).lower().strip()) < args.distance:
                print u'similarity of "%s" to "%s" in "%s' % (b, g, f)
            if args.regex:
                m=rx.match(g)
                if m is not None:
                    print u'regex match of "%s": %s in %s' % (b, g, f)
                    
#if len(args.line) == 0:
    #while True:
        #bbs = sys.stdin.readline()
        #if not bbs:
            #break
        #if (len(bbs) < 2) or (bbs is None):
            #continue
        #for f,goodlist in tlists.items():
            #for g in goodlist:
                #b=bbs.decode(sys.stdin.encoding if sys.stdin.encoding else 'UTF-8')
                #if Levenshtein.distance(g.lower().strip(),unicode(b).lower().strip()) < args.distance:
                    #print u'similarity of "%s" to "%s" in "%s' % (b, g, f)
