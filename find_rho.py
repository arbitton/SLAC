#!/usr/bin/env python

import sys
import re
from numpy import square, sqrt

def calculate(file):

   file_contents = open(file, 'r')

   xy_re = re.compile("[0-9]+\s(?P<clicks>[0-9]+)\s(?P<cites>[0-9]+)")

   x = []
   y = []

   for line in file_contents:
      xy_match = xy_re.search(line)
      if xy_match:
         x.append(int(xy_match.group('clicks')))
         y.append(int(xy_match.group('cites')))

   sum_xy = 0
   for i in range(0, len(x)):
         sum_xy += x[i]*y[i]

   x_square = float(sum(square(x)))
   y_square = float(sum(square(y)))

   result = (sum_xy - (sum(x)*sum(y))/float(len(x)))
   result = result/(sqrt((x_square - x_square/len(x)) * (y_square - y_square/len(y))))

   return result

def main(args):

   for file in args:
      rho = calculate(file)

   print "Pearson's Coefficient:", rho

if __name__ == "__main__":
   main(sys.argv[1:])
