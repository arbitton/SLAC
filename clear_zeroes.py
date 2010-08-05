#!/usr/bin/env python

import sys
import re

def main(args):

   line_re = re.compile("[0-9]+\s+(?P<click>[0-9]+)\s+(?P<cite>[0-9]+)")

   for file in args:
      file_contents = open(file, 'r')

      for line in file_contents:
         line_match = line_re.match(line)
         if line_match:
            if int(line_match.group('click')) > 10 and int(line_match.group('cite')) > 10:
               print line,


if __name__ == "__main__":
   main(sys.argv[1:])
