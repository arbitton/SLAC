#!/usr/bin/env python

import sys
import re

line_pattern = re.compile("(?P<click>[0-9]+)\s(?P<cite>[0-9]+)\s(?P<count>[0-9]+)")



def main(args):
   for file in args:

      file_contents = open(file, 'r')

         for line in file:   
            line_match = line_pattern.match(line)
            
            if line_match:
               x = int(line_match.group('click'))
               y = int(line_match.group('cite'))

               z = int(line_match.group('count')) # subtract expected value from x and y

               print x, y, z


if __name__ == "__main__":
   main(sys.argv[1:])
