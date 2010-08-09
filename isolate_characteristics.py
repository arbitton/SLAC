#!/usr/bin/env python

import sys
import re
from invenio.search_engine import get_fieldvalues

line_re = re.compile("(?P<click>[0-9]+)\s(?P<cite>[0-9]+)\s(?P<count>[0-9]+)\s\[(?P<paper_list>[,0-9\s]*)\]")
list_re = re.compile("[\b\]\[,\s]+")

def do_stuff(file):

   file_contents = open(file, 'r')

   for line in file_contents:

      match = line_re.match(line)

      if match:
         click = int(match.group('click'))
         cite = int(match.group('cite'))
         count = int(match.group('count'))
         if count != 0:
            review_count = 0
            paper_list = list_re.split(match.group('paper_list'))
            for x in paper_list:
               if 'Review' in get_fieldvalues(int(x), '980__%'):
                  review_count += 1
            print click, cite, review_count
         else:
            print click, cite, "0"


def main(args):

   for file in args:

      do_stuff(file)

if __name__ == "__main__":
   main(sys.argv[1:])
