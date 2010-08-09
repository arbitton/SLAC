#!/usr/bin/env python

import sys
import re
from invenio.search_engine import get_fieldvalues
from invenio.bibrank_citation_searcher import get_cited_by_count

def read_data(file, overall_dict):
   """Open each file, and pull the cites and clicks from each line. Then consolidate
   the data into the new dictionary overall_dict by eliminating the rec id and
   grouping items by their clicks and citations - creating a new count.
   """

   file_contents = open(file, 'r')

   clicks_re = re.compile("(?P<rid>[0-9]+)\s(?P<clicks>[0-9]+)\s(?P<cites>[0-9]+)")

   for line in file_contents:
      line_match = clicks_re.search(line)

      if line_match:
#         rid = int(line_match.group('rid'))
#         if 'Review' in get_fieldvalues(rid, '980__%'):
#            print rid, get_fieldvalues(rid, '980__%')
#         if get_cited_by_count(rid) > 100:
            rid = int(line_match.group('rid'))
            clicks = int(line_match.group('clicks'))
            cites = int(line_match.group('cites'))
            if clicks not in overall_dict:
               overall_dict[clicks] = {cites: [rid]}
            elif cites not in overall_dict[clicks]:
               overall_dict[clicks][cites] = [rid]
            else:
               overall_dict[clicks][cites].append(rid)

   return overall_dict

def grid_data(overall_dict):
   # bin size: 2
   # i = (i * n) to (i * (n + 1) - 1) 
   # read dict, placing items in bins
   # add zeroes?

#   grid_dict = {0: {0: 0}}   
   grid_dict = overall_dict
   largest_cites = 0

   for clicks in overall_dict:
      largest_clicks = clicks
      for cites in overall_dict[clicks]:
         if cites > largest_cites:
            largest_cites = cites
#         largest_clicks = (clicks + 1)/2
#         if (cites + 1)/2 > largest_cites:
#            largest_cites = (cites + 1)/2
#         if (clicks + 1)/2 not in grid_dict:
#            grid_dict[(clicks + 1)/2] = {(cites + 1)/2: overall_dict[clicks][cites]}
#         elif (cites + 1)/2 not in grid_dict[(clicks + 1)/2]:
#            grid_dict[(clicks + 1)/2][(cites + 1)/2] = overall_dict[clicks][cites]
#         else:
#            grid_dict[(clicks + 1)/2][(cites + 1)/2] += overall_dict[clicks][cites]

   # insert the implicit zeroes into the grid
   for x in range(0, largest_clicks + 1):
      for y in range(0, largest_cites + 1):
         if (x not in grid_dict):
            grid_dict[x] = {y: []}
         elif y not in grid_dict[x]:
            grid_dict[x][y] = []

   return grid_dict


def print_data(overall_dict):
   """Print the data set compiled in read_data."""

   test = 0
   total_clicks = 0

   for clicks in overall_dict:
      print " "
      for cites in overall_dict[clicks]:
         #print clicks, cites, frequency
         print "%d %d %d" % (clicks, cites, len(overall_dict[clicks][cites])), overall_dict[clicks][cites]
         total_clicks += clicks * len(overall_dict[clicks][cites])
         test += len(overall_dict[clicks][cites])

   #print total of summed frequency (ie total number of papers)
   print "# Total papers:", test
   print "# Total clicks:", total_clicks

def main(args):
   #overall dict: {clicks: {citations: count}}
   overall_dict = {0: {0: []}, 1: {0: []}, 2: {0: []}}

   for file in args:
      overall_dict = read_data(file, overall_dict)

   overall_dict = grid_data(overall_dict)

   print_data(overall_dict)

if __name__ == "__main__":
   main(sys.argv[1:])
