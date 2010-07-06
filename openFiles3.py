#! /usr/bin/python

from invenio.search_engine import perform_request_search

import re
from urllib import unquote_plus

def printFile(n):
   f = open(n, 'r')
   print f
   
   search = perform_request_search

   p = re.compile('outgoing')
   pA = re.compile("outgoing/[0-9a-zA-Z\.:\-/]*")
   count = 0
   idsFound = 0
   list = []
   urls = {}

   for line in f:
      line = unquote_plus(line)
      m = p.search(line)
      if m:
         #print 'Match found:', m.group()
         mA = pA.search(line)
         if mA:
            #print "ID:", mA.group(), "\n"
            idsFound += 1
            list.append(mA.group())
            if mA.group() not in urls:
               urls[mA.group()] = 1
            else:
               urls[mA.group()] = urls[mA.group()] + 1
         count += 1

   print "Total outgoing clicks:", count
   print "URLs found:", idsFound
   #for x in list:
   #   print x, list.count(x)
   print "Total items:", len(urls)

   urlKeys = urls.iterkeys()
   urlAppearances = urls.itervalues()
    
   print "Clicks:", "Paper ID:"
   for k in urls:
     print repr(urlAppearances.next()).rjust(7), urlKeys.next()

   a = re.compile("arx/[a-z-]+/(?P<rid>[0-9]{4}\.[0-9]+)")
   b = re.compile("arx/(abs|pdf|ps)/(?P<rid>(hep|astro|nucl|gr|quant|cond)-(ph|th|qc|lat|ex|mat)/[0-9]{7})")
   c = re.compile("doi/[0-9\.]+/(?P<rid>physrevd[0-9a-z/\.]*)")
   #regex = {a: "arxiv:" + result.group('rid')}
   regex = {a: "arxiv:", b: "", c: ""}
   rec_ids = {}

   tests = {1: (lambda match: "arxiv:" + match.group('rid')), 2: "hello"}
   count = 0

   for k in urls:
      hey = False
      count += 1
      for pattern in regex:
         result = pattern.search(k)
         if result:
            hey = True
            print result.group('rid')
            search_results = perform_request_search(p=regex[pattern] + result.group('rid'))
            if count == 2:
               print "Hello:", tests[1](result)
               search_results2 = perform_request_search(p=tests[1](result))
               print "Work please:", search_results2
            print search_results
            if len(search_results) != 1:
               #regex dictionary needs work
               print "Make regex for", k
            else:
               if search_results[0] not in rec_ids:
                  rec_ids[search_results[0]] = urls[k]
               else:
                  rec_ids[search_results[0]] += urls[k]
      if hey == False:
         print result, k
#         if result:
#            searchResults = perform_request_search(p=regex[pattern])
#            print searchResults
#            if len(searchResults) != 1:
#               #regex dictionary needs work
#               print "Make regex for:", k
#            elif len(searchResults) == 1:
#               # :)
#               if searchResults[0] not in recIDs:
#                  redIDs[searchResults[0]] = urls[k]
#               else:
#                  redIDs[searchResults[0]] += urls[k]
   print rec_ids
