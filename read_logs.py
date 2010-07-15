#!/usr/bin/env python

from invenio.search_engine import perform_request_search
from invenio.bibrank_citation_searcher import get_cited_by_count
import sys
import re
from urllib import unquote_plus
from invenio.bibrank_citation_searcher import get_cited_by

#regex is a dictionary holding all the possible regular expressions that can be taken from
#the urls to search and find the associated rec id of the actual paper. rhe keys of (the regex
#dictionary are the possible regular expressions and the values are how to format them to
#retrive the appropriate paper when using the function 'perform_request_search'
arxiv_general_pattern = re.compile("arx/(mirr/)*[a-z-]+/(?P<rid>[0-9]{4}\.[0-9]+)")
arxiv_secondary_general_pattern = re.compile("arx/(mirr/)*((abs|pdf|ps)/)*(?P<rid>[a-z/0-9-]+)")
arxiv_specific_pattern = re.compile("arx/(mirr/)*((abs|pdf|ps)/)*(?P<rid>(hep|astro|nucl|gr|quant|cond)-(ph|th|qc|lat|ex|mat)/[0-9]{7})")
doi_pattern = re.compile("doi/(http://dx.doi.org/)*[0-9\.]+/(?P<rid>[a-z\.0-9/)(-]*)")
physrevlett_pattern = re.compile("doi/(http://dx.doi.org/)*(?P<rid>[0-9.]{7}/(physrevd|j.physrep|physrev|aph|ptps|epjc/s|j.nuclphysb|j.physletb|physics|physrevlett|j.astropartphys|j.nuclphysbps).[0-9./-]+)")
doi_general_pattern = re.compile("doi/(http://dx.doi.org/)*(?P<rid>[0-9)(/.-]+)")
regex = {arxiv_specific_pattern: (lambda match: '037:' + match.group('rid')),
         arxiv_secondary_general_pattern: (lambda match: '037:' + match.group('rid')),
         arxiv_general_pattern: (lambda match: '"arxiv:' + match.group('rid') + '"'), 
         doi_pattern: (lambda match: (((((match.group('rid')).replace("/", " ")).replace("-", " ")).replace(".", " ")).replace(")", " ")).replace("(", " ")),
         physrevlett_pattern: (lambda match: '773:' + match.group('rid')), 
         doi_general_pattern: (lambda match: match.group('rid')),
        }

def dissect_log(n, rec_ids):

   for line in log_url_filter(n):
      rec_ids = url_count(line, rec_ids)
   
   return rec_ids

def log_url_filter(n):
   log_file = open(n, 'r')
   
   url_pattern = re.compile("outgoing/[0-9a-zA-Z\.:\-/]*")

   for line in log_file:
      line = unquote_plus(line)
      url_match = url_pattern.search(line)
      if url_match:
         yield line

def url_count(url_line, rec_ids):
  
   pattern_found = False

   for pattern in regex:
      result = pattern.search(url_line)
      if result and pattern_found == False:
         search_results = perform_request_search(p=regex[pattern](result))
         #print search_results
         #print result.group('rid')
         #print regex[pattern](result)
         #if len(search_results) != 1:
            #sys.stderr.write("Found search term: " + regex[pattern](result) + "\n")
            #sys.stderr.write("Number of search results: " + str(len(search_results)) + "\n")
            ##regex dictionary needs work
            #if len(search_results) < 100 and len(search_results) != 0:
               #sys.stderr.write(str(search_results))
         if len(search_results) == 1:
            pattern_found = True
            if search_results[0] not in rec_ids:
               rec_ids[search_results[0]] = 1
            else:
               rec_ids[search_results[0]] += 1

   #display the url if no pattern in the regex dictionary matched it
   if pattern_found == False:
      sys.stderr.write("NO MATCH: " + url_line + "\n")
   return rec_ids

def print_rec_ids(rec_ids):
   """Write something here"""

   complete_paper_list = perform_request_search(p='year:2009->2010')

   print "Rec ID, Clicks, All Citations, Narrowed Citations:"

   for key in rec_ids:
      narrowed_citation_list = []
      paper_citation_list = get_cited_by(key)

      for paper in paper_citation_list:
         if paper in complete_paper_list:
             narrowed_citation_list.append(paper)

      print "%d,%d,%d,%d" % (key, rec_ids[key], get_cited_by_count(key), len(narrowed_citation_list))

def main(args):
   rec_ids = {}

   for file in args:
      rec_ids = dissect_log(file, rec_ids)

   print_rec_ids(rec_ids)

if __name__ == "__main__":
   main(sys.argv[1:])
