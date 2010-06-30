#! /usr/bin/python

import re
from urllib import unquote_plus

def printFile(n):
   f = open(n, 'r')
   print f
   
   p = re.compile('outgoing')
   pA = re.compile("outgoing/[0-9a-zA-Z\.:\-/]*")
   count = 0
   idsFound = 0
   list = []
   a = {}

   for line in f:
      line = unquote_plus(line)
      m = p.search(line)
      if m:
         print 'Match found:', m.group()
         print line
         mA = pA.search(line)
         if mA:
            print "ID:", mA.group(), "\n"
            idsFound += 1
            list.append(mA.group())
            if mA.group() not in a:
               a[mA.group()] = 1
            else:
               a[mA.group()] = a[mA.group()] + 1
         count += 1
   print "Total outgoing clicks:", count
   print "IDs found:", idsFound
   #for x in list:
   #   print x, list.count(x)
   print "Total items:", len(a)
   c = a.iterkeys()
   d = a.itervalues()
   print "Clicks:", "Paper ID:"
   for k in a:
   #  print '{0:7} {1:5}'.format(l, k)
     print repr(d.next()).rjust(7), c.next()
