#! /usr/bin/python

from invenio.search_engine import perform_request_search

import re
from urllib import unquote_plus

def printFile(n):
   log_file = open(n, 'r')
   print log_file
   
   search = perform_request_search

   url_pattern = re.compile("outgoing/[0-9a-zA-Z\.:\-/]*")
   click_count = 0
   url_list = []
   urls = {}

   for line in log_file:
      line = unquote_plus(line)
      url_match = url_pattern.search(line)
      if url_match:
         #print 'Match found:', url_match.group(), "\n"
         click_count += 1
         url_list.append(url_match.group())
         if url_match.group() not in urls:
            urls[url_match.group()] = 1
         else:
            urls[url_match.group()] = urls[url_match.group()] + 1

   print "Total outgoing clicks:", click_count
   #for x in url_list:
   #   print x, list.count(x)
   print "Total distinct clicks:", len(urls)

   urlKeys = urls.iterkeys()
   urlAppearances = urls.itervalues()
    
   print "Clicks:", "Paper ID:"
   for k in urls:
     print repr(urlAppearances.next()).rjust(7), urlKeys.next()

   a = re.compile("arx/[a-z-]+/(?P<rid>[0-9]{4}\.[0-9]+)")
   regex = {a: (lambda match: "arxiv:" + match.group('rid'))}
   b = re.compile("arx/(abs|pdf|ps)/(?P<rid>(hep|astro|nucl|gr|quant|cond)-(ph|th|qc|lat|ex|mat)/[0-9]{7})")
   regex[b] = (lambda match: match.group('rid'))
   c = re.compile("doi/[0-9\.]+/(?P<rid>physrevd)\.(?P<rid2>[0-9]*)\.(?P<rid3>[0-9]*)")
   regex[c] = (lambda match: match.group('rid') + " " + match.group('rid2') + " " + match.group('rid3'))

   rec_ids = {}

   tests = {1: (lambda match: "arxiv:" + match.group('rid')), 2: "hello"}

   for k in urls:
      pattern_found = False
      for pattern in regex:
         result = pattern.search(k)
         if result:
            pattern_found = True
            print result.group()
            search_results = perform_request_search(p=regex[pattern](result))
            print search_results
            if len(search_results) != 1:
               #regex dictionary needs work
               print "Make regex for", k
            else:
               if search_results[0] not in rec_ids:
                  rec_ids[search_results[0]] = urls[k]
               else:
                  rec_ids[search_results[0]] += urls[k]
      if pattern_found == False:
         print "No pattern found for:", k, result
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
