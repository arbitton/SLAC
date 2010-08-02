#!/usr/bin/env python

from invenio.search_engine import perform_request_search
from invenio.bibrank_citation_searcher import get_cited_by_count
import sys
import re
from urllib import unquote_plus

#regex is a dictionary holding all the possible regular expressions that can be taken from
#the urls to search and find the associated rec id of the actual paper. the keys of the regex
#dictionary are the possible regular expressions and the values are how to format them to
#retrive the appropriate paper when using the function 'perform_request_search'
arxiv_general_pattern = re.compile("arx/[a-z-]+/(?P<rid>[0-9]{4}\.[0-9]+)")
arxiv_specific_pattern = re.compile("arx/(abs|pdf|ps)/(?P<rid>(hep|astro|nucl|gr|quant|cond)\-(ph|th|qc|lat|ex|mat)/[0-9]{7})")
doi_pattern = re.compile("doi/[0-9\.]+/(?P<rid>[a-z\.0-9/)(-]*)")
regex = {arxiv_specific_pattern: (lambda match: '037:' + match.group('rid')),
         arxiv_general_pattern: (lambda match: '"arxiv:' + match.group('rid') + '"'), 
         doi_pattern: (lambda match: (((((match.group('rid')).replace("/", " ")).replace("-", " ")).replace(".", " ")).replace(")", " ")).replace("(", " ")),
        }

blacklisted_ips = ["130.199.3.130", "128.250.54.23", "189.50.0.3", "156.35.192.2", "84.237.121.107", "140.105.47.82", "143.233.250.165", "147.46.56.157", "129.186.151.231", "210.117.131.100", "131.220.8.9", "221.116.19.146", "129.13.72.198", "130.199.3.140", "195.251.115.254", "122.130.177.184", "134.107.3.147", "193.206.153.230", "200.145.46.252", "149.156.47.236", "131.111.16.20", "192.16.204.74", "129.104.3.5", "202.41.93.129", "218.130.209.108", "194.80.32.11", "210.210.15.150", "129.70.124.44", "162.105.246.189", "192.16.204.77", "132.77.4.129", "132.77.4.43", "141.2.247.4", "147.156.163.88", "140.105.47.84", "194.94.224.254", "155.230.152.39", "129.234.4.76", "130.54.55.3", "149.217.1.6", "129.2.175.71", "130.225.212.4", "163.239.43.45", "210.219.50.14", "220.227.103.131", "129.234.4.10", "155.230.153.238", "159.93.14.8", "38.117.109.20", "202.160.174.4", "202.122.32.131"]

def dissect_log(n, rec_ids):

   for line in log_url_filter(n):
      rec_ids = url_count(line, rec_ids)
   
   return rec_ids

def log_url_filter(n):
   log_file = open(n, 'r')
   
   url_pattern = re.compile("Pid\s[0-9]+\s(?P<ip_add>[0-9.]+)\s.*outgoing/[0-9a-zA-Z\.:\-/]*")

   for line in log_file:
      line = unquote_plus(line)
      #SEARCH FOR PATTERN
      # if found, yield the line
      # if not, send line to stderr
      url_match = url_pattern.search(line)
      if url_match:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
         yield line
=======
=======
>>>>>>> f13a585... Creating program to read arXiv logs
=======
>>>>>>> f13a585... Creating program to read arXiv logs
         if url_match.group('ip_add') not in blacklisted_ips:
            yield line
   log_file.close()
>>>>>>> f13a585... Creating program to read arXiv logs

def url_count(url_line, rec_ids):
  
   pattern_found = False

   for pattern in regex:
      result = pattern.search(url_line)
      if result and pattern_found == False:
         search_results = perform_request_search(p=regex[pattern](result))
         if len(search_results) != 1:
            sys.stderr.write("Found search term: " + regex[pattern](result) + "\n")
            sys.stderr.write("Number of search results: " + str(len(search_results)) + "\n")
            #regex dictionary needs work
            if len(search_results) < 100 and len(search_results) != 0:
               sys.stderr.write(str(search_results))
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

   print "Rec ID, Clicks, Citations:"

   for key in rec_ids:
      print "%d,%d,%d" % (key, rec_ids[key], get_cited_by_count(key))

def main(args):
   rec_ids = {}

   for file in args:
      rec_ids = dissect_log(file, rec_ids)

   print_rec_ids(rec_ids)

if __name__ == "__main__":
   main(sys.argv[1:])
