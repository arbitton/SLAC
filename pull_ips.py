#!/usr/bin/env python

import sys
import re
from urllib import unquote_plus


def read_log(file, ip_dict):

   file_contents = open(file, 'r')

#   ip_re = re.compile("Pid\s[0-9]+\s(?P<ip_add>[0-9.]+)\s")
   ip_re = re.compile("Pid\s[0-9]+\s(?P<ip_add>[0-9.]+)\s.*utmp /outgoing/")

   for line in file_contents:
      line = unquote_plus(line)
      line_match = ip_re.search(line)
      if line_match:
         if line_match.group('ip_add') not in ip_dict:
            ip_dict[line_match.group('ip_add')] = 1
         else:
            ip_dict[line_match.group('ip_add')] += 1

   return ip_dict

def print_data(ip_dict):

   for ip in ip_dict:
      print ip_dict[ip], ip

def main(args):

   ip_dict = {}

   for file in args:
      ip_dict = read_log(file, ip_dict)

   print_data(ip_dict)

if __name__ == "__main__":
   main(sys.argv[1:])
