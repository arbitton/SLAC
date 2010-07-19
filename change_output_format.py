#!/user/bin/env python

import sys

def main(args):

    for file in args:
        log_file = open(file, 'r')

        for line in log_file:
           line = line.replace(",", " ")
           print line

if __name__ == "__main__":
   main(sys.argv[1:])
