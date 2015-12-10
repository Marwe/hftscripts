#! /usr/bin/env python
# -*- coding: utf-8 -*-
#from bs4 import BeautifulSoup
from BeautifulSoup import *
# ordered dictionary keeps insertion order
from collections import OrderedDict
# regex
import re
import argparse
import HTMLParser
import sys

parser = argparse.ArgumentParser(description='Process Thomsen Reuters Jounal Master list HTML to rst')
parser.add_argument(metavar='F', type=str, nargs='*', default=["index.html"], dest='filenames',
                   help='HTML files to be processed')
#parser.add_argument('-p', '--prefix', default='/tmp/', type=str, dest='prefix',
                   #help='prefix for the filenames of the results')
#parser.add_argument('-m', '--maxfilenamelenghth',default=127, type=int, choices=range(5,255), dest='maxlfn',
                   #help='maximum filename length')
parser.add_argument('-c', '--creole', action="store_true", dest='creole',
                   help='create creole output')
args = parser.parse_args()

def subtags(soup,tagid,subtagtype='span',sepstring=u', '):
    stout=u''
    foundtag=soup.find(id=tagid)
    if (foundtag is not None) and (len(foundtag.getText().strip()) > 0):
        keywords=foundtag.fetch(subtagtype)
        if len(keywords)>0:
                #outstring +=  u'* Schlagworte: '
                for keyword in keywords:
                        stout +=  cleanchars(keyword.getText())+sepstring
    return stout

class OutFormatter(object):
        headerlevelchar=(u'=', u'-', u'.', u'_', u'^')
        """ An output formatter class, defaults to rst markup """
        def bulletlistentry(self,text,level=None):
            if level is None:
                level=1
                #return u'* '+text+u'\n'
            blstring=u'  '*(level-1)
            blstring+=u'* '+text+u'\n'
            return blstring
        def header(self,text,level=None):
            if level is None:
                level=1
            hstring=text
            hstring+=u'\n'
            hstring+=self.headerlevelchar[level]*len(text.encode("utf-8"))+u'\n\n'
            return hstring
        def p(self):
            return u'\n\n'
        def url(self,url,linktext=None):
            if linktext is None:
                # nothing to change for rst
                return url
            else:
                utext=u'`'+linktext+u'<'+url+u'>`_'
            return utext
        def emph(self,text):
            return u'*'+text+u'*'
        def strongemph(self,text):
            return u'**'+text+u'**'

class OutFormatterCreole(OutFormatter):
        #headerlevelchar=(u'=', u'-', u'.', u'_', u'^')
        """ An output formatter class, creole markup """
        def bulletlistentry(self,text,level=None):
            if level is None:
                level=1
                #return u'* '+text+u'\n'
            blstring=u'*'*level
            blstring+=u' '+text+u'\n'
            return blstring
        def header(self,text,level=1):
            hstring=u'='*level
            hstring+=u' '
            hstring+=text+u'\n\n'
            #hstring+=headerlevelchar[level]*len(text.encode("utf-8"))+u'\n\n'
            return hstring
        def url(self,url,linktext=None):
            #[[link_address|link text]]
            utext=u'[['+url+u']]'
            if linktext is not None:
                utext=u'[['+url+u'|'+linktext+u']]'
            return utext
        def emph(self,text):
            return u'//'+text+u'//'
        # same as rst
        #def strongemph(self,text):
            #return u'**'+text+u'**'

of=OutFormatter()
if args.creole:
    print >> sys.stderr, u'using creole output'
    of=OutFormatterCreole()

for inputfile in args.filenames:
    print >> sys.stderr, u'reading '+inputfile
    outstring=u''
    soup = BeautifulSoup(open(inputfile),convertEntities=BeautifulSoup.HTML_ENTITIES)
    # title = unicode(cleanchars(soup.title.string))#.encode("utf-8")))

    # Jounal title enclosed in <DT><strong>
    foundtags=soup.findAll('dt')#(id=parsedictids[pid])
    for foundtag in foundtags:
        if (foundtag is not None) and (len(foundtag.getText().strip()) > 0):
            print of.bulletlistentry(foundtag.getText())
