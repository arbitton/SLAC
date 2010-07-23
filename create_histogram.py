#!/usr/bin/env python

import sys
import re

def read_data(file, overall_dict):
   """Open each file, and pull the cites and clicks from each line. Then consolidate
   the data into the new dictionary overall_dict by eliminating the rec id and
   grouping items by their clicks and citations - creating a new count.
   """


   file_contents = open(file, 'r')

   clicks_re = re.compile("[0-9]+\s(?P<clicks>[0-9]+)\s(?P<cites>[0-9]+)")

   for line in file_contents:
      line_match = clicks_re.search(line)

      if line_match:
         clicks = int(line_match.group('clicks'))
         cites = int(line_match.group('cites'))
         if clicks not in overall_dict:
            overall_dict[clicks] = {cites: 1}
         elif cites not in overall_dict[clicks]:
            overall_dict[clicks][cites] = 1
         else:
            overall_dict[clicks][cites] +=1

   return overall_dict

def grid_data(overall_dict):
   # bin size: 2
   # i = (i * n) to (i * (n + 1) - 1) 
   # read dict, placing items in bins
   # add zeroes?

   grid_dict = {0: {0: 0}}

   for clicks in overall_dict:
      for cites in overall_dict[clicks]:
         largest_clicks = clicks/2
         largest_cites = cites/2
         if clicks/2 not in grid_dict:
            grid_dict[clicks/2] = {cites/2: overall_dict[clicks][cites]}
         elif cites/2 not in grid_dict[clicks/2]:
            grid_dict[clicks/2][cites/2] = overall_dict[clicks][cites]
         else:
            grid_dict[clicks/2][cites/2] += overall_dict[clicks][cites]

   # insert the implicit zeroes into the grid
   for x in range(0, largest_clicks):
      for y in range(0, largest_cites):
         if (x not in grid_dict):
            grid_dict[x] = {y: 0}
         elif y not in grid_dict[x]:
            grid_dict[x][y] = 0

   return grid_dict

def print_data(overall_dict):
   """Print the data set compiled in read_data."""

   test = 0

   for clicks in overall_dict:
      for cites in overall_dict[clicks]:
         #print clicks, cites, frequency
         print "%d %d %d" % (clicks, cites, overall_dict[clicks][cites])
         test += overall_dict[clicks][cites]

   #print total of summed frequency (ie total number of papers)
   print "Test:", test

def main(args):
   #overall dict: {clicks: {citations: count}}
   overall_dict = {0: {0: 0}, 1: {0: 0}, 2: {0: 0}}

   for file in args:
      overall_dict = read_data(file, overall_dict)

   overall_dict = grid_data(overall_dict)

   print_data(overall_dict)

if __name__ == "__main__":
   main(sys.argv[1:])
