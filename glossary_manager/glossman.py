#!/bin/python
##############################################################################
"""
Administer and manage the contents of a custom glossary stored as .csv file.
Written for Python 3.4.
"""

import csv
import getopt
import sys
from Glossary import Glossary

def print_status(text):
    print('### '+text+' ###')

def usage():
    print("""glossary_manager -a [tags|terms] [-h] -i inputFile [-o outputFile] [-t term]
    -a, --all        : print all terms or tags.
    -h, --help       : print this help text
    -i, --inputFile  : input CSV file name
    -o, --outputFile : output CSV file name
    -t, --term       : term to look up in glossary, may occur multiple times
    """)

if __name__ == '__main__':
    inputFile = ''
    outputFile = ''
    lookupTerms = []
    printTags = False
    printTerms = False
    
    # Parse command line arguments.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:hi:o:t:',
            ['all', 'help', 'inputFile=', 'outputFile=', 'term='])
    except Exception as e:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-a', '--all'):
            if arg == 'tags':
                printTags = True
                continue
            if arg == 'terms':
                printTerms = True
                continue
            usage()
            sys.exit(2)
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-i', '--inputFile'):
            inputFile = arg
        if opt in ('-o', '--outputFile'):
            outputFile = arg
        if opt in ('-t', '--term'):
            lookupTerms.append(arg)
    
    if (inputFile == '' or (len(lookupTerms) == 0 and \
        not (printTags or printTerms))):
            usage()
            sys.exit(2)
    
    print_status("Starting glossary_manager")
    
    # Create glossary.
    print_status('Creating Glossary object.')
    g = Glossary()
    
    # Read contents of the .csv file.
    g.read_csv(inputFile)
    print_status("Read "+str(len(g.get_terms()))+" glossary entries.")
    
    # Lookup terms in glossary.
    if len(lookupTerms) > 0:
        print_status('Retrieving glossary entries.')
        for t in lookupTerms:
            print(g.get(str(t)))
    
    # Print tags and/or terms defined in glossary.
    if printTags:
        print_status('Printing tags.')
        l = list(g.get_terms())
        l.sort()
        print(l)
        
    if printTerms:
        print_status('Printing terms.')
        l = list(g.get_terms())
        l.sort()
        print(l)
    
    # Open output file.
    if outputFile != '':
        g.write_csv(outputFile)
    
    print_status("Exiting glossary_manager")
    
