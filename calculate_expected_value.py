#!/usr/bin/env python

import sys
import re

line_pattern = re.compile("(?P<click>[0-9]+)\s(?P<frequency>[0-9]+)")

def main(file):

   file_contents = open(file, 'r')

   y_list = []

   for line in file_contents:

      line_match = line_pattern.match(line)
      if line_match:

         x = int(line_match.group('click'))
         y = int(line_match.group('frequency'))

         y_list.append(y)

   total_clicks = sum(y_list)
   result = {}

   for i in range(0, len(y_list)):

      result[i] = float(y_list[i])/total_clicks

   print result

if __name__ == "__main__":
   main(sys.argv[1])
