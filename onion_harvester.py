#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 01:14:03 2017

@author: mheinl
"""

from google import search
import requests, re, getopt, sys

harvest = []
inputfile = ''
outputfile = 'harvest.txt'
googleSearchTerm = 'onion links'

help = '\nUsage: onion_harvester.py [options]\n'\
       'Options:\n'\
       '-h \t \t \t Show this help\n'\
       '-i \t <inputfile> \t Read URLs from inputfile\n'\
       '-o \t <outputfile> \t Write harvested onions to outputfile (default: harvest.txt)\n'\
       '-s \t <searchterm> \t Harvest Google search results (default: \'onion links\')'

### Handle options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:o:s:")
except getopt.GetoptError:
    print(help)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(help)
        sys.exit()
    elif opt in ('-o'):
        outputfile = arg
    elif opt in ('-i'):
        inputfile = arg
    elif opt in ('-s'):
        googleSearchTerm = arg
        
        
### Send request, parse response, write in harvest
def harvester (website):
    print('[+] scan ' + website.rstrip())
    try:
        page = requests.get(website.rstrip())
        onions = re.findall('([0-9a-z]{16}).onion', page.text)
        harvest.extend(onions)
    except requests.exceptions.RequestException as e:
        print('[-] Error: ' + str(e)) 
    
    
### If passed, read URLs from file
if inputfile:
    file = open(inputfile, 'r')
    print('[+] Harvest URLs from ' + inputfile + ':')
    for website in file:
        harvester(website)
        

### read URLs directly from google
print('[+] Harvest URLs from Google:')
for website in search(googleSearchTerm, stop=1):
    harvester(website)


### Treat the Harvest
harvest = (set(harvest)) # convert to set terminating doubles
print('[+] write ' + str(len(harvest)) + ' unique identifiers to ' + outputfile)
out = open(outputfile,'w')
for element in harvest:
    out.write("%s\n" % element)
print('[+] Done!')