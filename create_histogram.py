#!/usr/bin/env python

import sys
import re

def do_stuff(file, overall_dict):
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

def print_data(overall_dict):

   test = 0

   for clicks in overall_dict:
      for cites in overall_dict[clicks]:
         print "%d %d %d" % (clicks, cites, overall_dict[clicks][cites])
         test += overall_dict[clicks][cites]

   print "Test:", test

def main(args):
   #overall dict: {(clicks, cites): count}
   #overall dict: {clicks: {citations: count}}
   overall_dict = {1: {0: 0}, 2: {0: 0}}

   for file in args:
      overall_dict = do_stuff(file, overall_dict)

   print_data(overall_dict)

if __name__ == "__main__":
   main(sys.argv[1:])
