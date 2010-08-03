#!/usr/bin/env python

import sys
import re
from random import shuffle

def main(args):

   line_re = re.compile("(?P<recid>[0-9]+)\s+(?P<click>[0-9]+)\s+(?P<cite>[0-9]+)")

   recids = []
   clicks = []
   cites = []

   for file in args:

      file_contents = open(file, 'r')
      
      for line in file_contents:
         
         line_match = line_re.search(line)

         if line_match:
            recids.append(int(line_match.group('recid')))
            clicks.append(int(line_match.group('click')))
            cites.append(int(line_match.group('cite')))

      x = len(recids)

      shuffle(cites)

      for i in range(0, x):
         print recids[i], clicks[i], cites[i]

if __name__ == "__main__":
   main(sys.argv[1:])
