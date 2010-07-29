#!/usr/bin/env python

import sys
import re

def count_clicks(file, clicks_dict):
   
   file_contents = open(file, 'r')

   clicks_re = re.compile("(?P<clicks>[0-9]+)\s[0-9]+\s(?P<count>[0-9]+)")

   for line in file_contents:
      line_match = clicks_re.search(line)

      if line_match:
         clicks = int(line_match.group('clicks'))
         count = int(line_match.group('count'))

         if clicks not in clicks_dict:
            clicks_dict[clicks] = count
         else:
            clicks_dict[clicks] += count

   return clicks_dict

def count_cites(file, cites_dict):

   file_contents = open(file, 'r')

   cites_re = re.compile("[0-9]+\s(?P<cites>[0-9]+)\s(?P<count>[0-9]+)")

   for line in file_contents:
      line_match = cites_re.search(line)

      if line_match:
         cites = int(line_match.group('cites'))
         count = int(line_match.group('count'))

         if cites not in cites_dict:
            cites_dict[cites] = count
         else:
            cites_dict[cites] += count

   return cites_dict

def print_data(final_dict):

   for x in final_dict:
      print x, final_dict[x]

def main(args):

   final_dict = {}
   
   for file in args:
      final_dict = count_cites(file, final_dict)

   print_data(final_dict)

if __name__ == "__main__":
   main(sys.argv[1:])
