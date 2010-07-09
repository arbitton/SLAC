#!/usr/bin/env python

from invenio.search_engine import perform_request_search
from invenio.bibrank_citation_searcher import get_cited_by_count
import sys
import re
from urllib import unquote_plus

def dissect_log(file_name, rec_ids):
   """Write something here"""

   file_urls = read_log_file(file_name)
   return  fill_rec_id_dictionary(rec_ids, file_urls)

def read_log_file(n):
   """Write something here"""
   log_file = open(n, 'r')
   
   url_pattern = re.compile("outgoing/[0-9a-zA-Z\.:\-/]*")
   click_count = 0
   urls = {}

   for line in log_file:
      line = unquote_plus(line)
      url_match = url_pattern.search(line)
      if url_match:
         #print 'Match found:', url_match.group(), "\n"
         click_count += 1
         if url_match.group() not in urls:
            urls[url_match.group()] = 1
         else:
            urls[url_match.group()] = urls[url_match.group()] + 1

   print "Total outgoing clicks:", click_count, "\n"

   return urls

def fill_rec_id_dictionary(rec_ids, urls):
   """Write something here"""

   #regex is a dictionary holding all the possible regular expressions that can be taken from
   #the urls to search and find the associated rec id of the actual paper. the keys of the regex
   #dictionary are the possible regular expressions and the values are how to format them to
   #retrive the appropriate paper when using the function 'perform_request_search'
   a = re.compile("arx/[a-z-]+/(?P<rid>[0-9]{4}\.[0-9]+)")
   regex = {a: (lambda match: "arxiv:" + match.group('rid'))}
   b = re.compile("arx/(abs|pdf|ps)/(?P<rid>(hep|astro|nucl|gr|quant|cond)-(ph|th|qc|lat|ex|mat)/[0-9]{7})")
   regex[b] = (lambda match: match.group('rid'))
   #c = re.compile("doi/[0-9\.]+/(?P<rid>physrevd\.[0-9a-z]*\.[0-9a-z]*)")
   #regex[c] = (lambda match: (match.group('rid')).replace("." or "/", " " ))
   c = re.compile("doi/[0-9\.]+/(?P<rid>[a-z\.0-9/-]*)")
   regex[c] = (lambda match: (((match.group('rid')).replace("/", " ")).replace("-", " ")).replace(".", " "))

   total_rec_ids = 0
   total_failed_urls = 0

   for k in urls:
      pattern_found = False
      for pattern in regex:
         result = pattern.search(k)
         if result:
            search_results = perform_request_search(p=regex[pattern](result))
            if len(search_results) != 1:
               print "Found search term:", regex[pattern](result)
               #regex dictionary needs work
               if len(search_results) > 100:
                  print "Search results are very long"
               elif len(search_results) == 0:
                  print "Search returned no results for:"
            else:
               pattern_found = True
               if search_results[0] not in rec_ids:
                  total_rec_ids += 1
                  rec_ids[search_results[0]] = urls[k]
               else:
                  rec_ids[search_results[0]] += urls[k]
      #display the url if no pattern in the regex dictionary matched it
      if pattern_found == False:
         total_failed_urls += 1
         sys.stderr.write("No Match: " + k + "\n\n")
   print "Total rec ids:", total_rec_ids
   print "Total failed URLS:", total_failed_urls
   
   return rec_ids
   
def print_rec_ids(rec_ids):
   """Write something here"""

   print "Clicks, Rec ID, Citations:"

   for key in rec_ids:
      print "%d,%d,%d" % (rec_ids[key], key, get_cited_by_count(key))

def main(args):
   rec_ids = {}

   for file in args:
      rec_ids = dissect_log(file, rec_ids)

   print_rec_ids(rec_ids)

if __name__ == "__main__":
   main(sys.argv[1:])
