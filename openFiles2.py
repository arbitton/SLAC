#! /usr/bin/python

import re
from urllib import unquote_plus

def printFile(n):
   f = open(n, 'r')
   print f
   
   p = re.compile('outgoing')
   p1 = re.compile("[0-9]{4}\.[0-9]{4}")
   p2 = re.compile("hep-(t|p)h/[0-9]{7}")
   p3 = re.compile("doi/[0-9]{2}\.[0-9]{4}/[0-9a-zA-Z\.]*")
   p4 = re.compile("gr-qc/[0-9]{7}")
   p5 = re.compile("doi/[0-9]{2}\.[0-9]{4}/physrevd\.[0-9]{2}\.[0-9]{3,4}")
   p6 = re.compile("astro-ph/[0-9]{7}")
   count = 0
   idsFound = 0

   for line in f:
      line = unquote_plus(line)
      m = p.search(line)
      if m:
         print 'Match found:', m.group()
         print line
         m1 = p1.search(line)
         m2 = p2.search(line)
         m3 = p3.search(line)
         m4 = p4.search(line)
         m5 = p5.search(line)
         m6 = p6.search(line)
         if m1:
            print "ID:", m1.group(), "\n"
            idsFound += 1
         elif m2:
            print "ID:", m2.group(), "\n"
            idsFound += 1
         elif m3:
            print "ID:", m3.group(), "\n"
            idsFound += 1
         elif m4:
            print "ID:", m4.group(), "\n"
            idsFound += 1
         elif m5:
            print "ID:", m5.group(), "\n"
            idsFound += 1
         elif m6:
            print "ID:", m6.group(), "\n"
            idsFound += 1
         count += 1
   print "Total outgoing clicks:", count
   print "IDs found:", idsFound
