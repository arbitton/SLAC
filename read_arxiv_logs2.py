#!/usr/bin/env python

from invenio.search_engine import perform_request_search
# from invenio.bibrank_citation_searcher import get_cited_by_count
from invenio.intbitset import intbitset
import sys
import re
# from urllib import unquote_plus
from invenio.bibrank_citation_searcher import get_cited_by
from invenio.search_engine import get_fieldvalues

#regex is a dictionary holding all the possible regular expressions that can be taken from
#the urls to search and find the associated rec id of the actual paper. rhe keys of (the regex
#dictionary are the possible regular expressions and the values are how to format them to
#retrive the appropriate paper when using the function 'perform_request_search'
# arxiv_general_pattern = re.compile("[a-z0-9]+\s*(?P<rid>[0-9]{4}\.[0-9]+)")
# arxiv_secondary_general_pattern = re.compile("[a-z0-9]+\s*(?P<rid>[a-z/0-9-]+)")
# arxiv_specific_pattern = re.compile("[a-z0-9]+\s*(?P<rid>(hep|astro|nucl|gr|quant|cond)-(ph|th|qc|lat|ex|mat)/[0-9]{7})")
# regex = {arxiv_specific_pattern: (lambda match: '037:' + match.group('rid')),
#          arxiv_secondary_general_pattern: (lambda match: '037:' + match.group('rid')),
#          arxiv_general_pattern: (lambda match: '"arxiv:' + match.group('rid') + '"'),
#         }

ip_pattern = re.compile("[0-9]+\s(?P<ip_add>[0-9a-z]+)\s")
recid_pattern = re.compile("(?P<recid>[0-9]+)\s")

blacklisted_ips = ["7786119ae", "d850ad5d8", "38d4282b4", "39c6080b5", "b6b7ffb56", "ffe4b5dd0", "b92e643dd", "bddcba68f", "15d5d8b71", "e945c4e2e", "ccc91fb83", "f1d348cde", "de50a87bc", "a3772a07a", "8ff3417e0", "fc7ce2fca", "fbe537527", "97176c939", "a2318f3a9", "ac63c3543", "c2669d469", "a39e51e79", "1b68c255c", "42322ce17", "b98217c3a", "87438682d", "957fff065", "a73454fa5", "e6c5bb7d4", "9ecdb49a5", "b06795480", "0e77ca2e5", "d19545f28", "cde731491", "a29e3f468", "eb55b4e93", "f5642bdd1", "7ca15c422", "aff1d19c5", "59b5ac183", "5131837db", "26282dfe2", "83559cbe2", "090a05ba1", "8880cc50f", "4e141decd", "3c8131926", "0d61906d0", "9122da39d", "09f4f0568", "be4a82014", "510192229", "0be7cda06", "6fc7559c3", "dd3a9f54b", "79016361c", "dee33ae1d", "20462553e", "dd64767f2", "29ac93c70", "9937bf8d4", "508819e09", "4c7d472b2", "c21811ca3", "2e52ef26c", "84f33c282", "bf43e524f", "c2dc51048", "f1393db59", "ba255e2e1", "33a8b3417", "71343d6ff", "940221264", "49d6fd26c", "3e387d192", "68e537963", "d256d102f", "3057324cb", "99d376256", "cde7060cb", "65c725625", "6f98e6fc4", "1219ea005", "c2f18c0f3", "9bb93eed5", "a742a0896", "220e91e7d", "79e7feb99", "c188cb304", "e925be648", "8ee9c8501", "918cb4642", "b11d0bca4", "9fc2db8e0", "b04b53270", "2ea199674", "5efaf606c", "5f1468b90", "9eb05031b", "1abf57857", "0a8945bc4", "3ee3d12f6", "6d7b05166", "7b0fccc8b", "f4f5c2eaf", "44c952a42", "a1eddc41e", "79b57eaeb", "71cacff6c", "94bf35740", "3430b27bf", "a0f67bec0", "273a495da", "e0381cc4b", "a00f177c9", "72e596fad", "fd0fa78d3", "2b2753160", "6197c8b9a", "0f8b88249", "939f2708c", "5b457ff9f", "ef90446b2", "5b726b25b", "f4917ecf5", "e5e544d85", "3649cb004", "d2106e7ae", "1be1b8f6a", "6c3546083", "663152d15", "0cc132f55", "58703f541", "ecb77020d", "b19746a77", "0498a6d3e", "ba1af667b", "751e303bf", "3bef910ee", "fcd677ce4", "8cbeae2d4", "ff5fa1633", "d08401cd8", "3c1ac9878", "d7c763504", "72a9cb58b", "61ae259d6", "8dee441f8", "d5c35d7f6", "8faaaf163", "e8cbccb03", "bdca4fd52", "7708eb376", "e991b49f7", "fffdb5d84", "c7932db16", "af57b8f3c", "d27859b6e", "cdf3d0df8", "701409677", "5da244944", "925bc3a9f", "22141d243", "326125291", "c11781384", "0e1b76e6c", "299448bfa", "f99efe00c", "362755b3e", "4ece74a13", "1820aef54", "c597dfdc5", "2f3a3b106", "d9ce861c6", "cef7f51da", "a74afc533", "0fc515ec2", "b6fc890d9", "c11f2699b", "88f5351ad", "41db2b021", "c9e913cdf", "a541e74b4", "d5393c773", "752cd517f", "58eb5a386", "20cf74dad", "306b26fe8", "e79f74cbc", "40f0be963", "4780773e1", "ca92a297e", "686d61802", "b073fa0eb", "56acd61ab", "973d40e15", "dcbb0a00d", "8f21e7fa5", "c0e29e525", "8fe48ed99"]

def dissect_log(n, rec_ids):

   for line in log_url_filter(n):
      rec_ids = url_count(line, rec_ids)

   return rec_ids

def log_url_filter(n):
   log_file = open(n, 'r')

   for line in log_file:
#      line = unquote_plus(line)
      ip_match = ip_pattern.match(line)
      if ip_match:
         if ip_match.group('ip_add') not in blacklisted_ips:
            yield line
   log_file.close()

def url_count(url_line, rec_ids):

   result = recid_pattern.match(url_line)
#  if fieldvalues_pass(search_results[0], ('2009-02', '2009-01', '2008-12')):
   if int(result.group('recid')) not in rec_ids:
      rec_ids[int(result.group('recid'))] = 1
   else:
      rec_ids[int(result.group('recid'))] += 1

   return rec_ids

def fieldvalues_pass(rid, filter_list):
   rid_fieldvalues = get_fieldvalues(rid, '269__c')
   if len(rid_fieldvalues) == 1:
      return rid_fieldvalues[0] in filter_list
   return False

def print_rec_ids(rec_ids):
   complete_paper_list = intbitset(perform_request_search(p='year:2009->2010'))

   print "# Rec ID, Clicks, Citations:"

   for key in rec_ids:

      paper_citation_list = intbitset(get_cited_by(key))

      narrowed_citation_count = len(paper_citation_list & complete_paper_list)
      print "%d %d %d" % (key, rec_ids[key], narrowed_citation_count)

def main(args):
   rec_ids = {}

   for file in args:
      rec_ids = dissect_log(file, rec_ids)

   print_rec_ids(rec_ids)

if __name__ == "__main__":
   main(sys.argv[1:])

