#!/bin/python

import csv
import glossary_manager.glossary_error

class Glossary(object):
    """A class holding a glossary and providing access to the content.
    
    A glossary entry consists of at least a term and a description.
    For improved managability one or more tags can be attached to a term.
    Additional items can be added to a glossary entry according to a given
    format specifier.
    
    Each glossary entry is represented by a list containing the term,
    a description, associated tags and additional items.
    The format of a glossary entry is fixed at the moment and looks like this:
    ['term', 'abbreviation', 'full name', 'tags', 'description']
    
    To store the glossary after processing, conversion functions are provided
    which support various output formats:
    - nothing
    
    Known issues: for now 'term' is the fixed primary key.
    """
    def __init__(self, glossary=[], entryFormat=None):
        self.content = []
        self.entryFormat = []
        
        if isinstance(glossary, list):
            self.add_list(glossary, entryFormat)
        elif isinstance(glossary, dict):
            self.add_dict(glossary)
        else:
            raise GlossaryError("Invalid argument type.")
        
        return
    
    def __notify(self, msg):
        print('### '+msg+' ###')
        return
    
    def add_list(self, L, entryFormat=None):
        """Add entries from a list of lists to the glossary."""
        entryAddCount = 0
        if len(L) > 0:
            if len(self.entryFormat) == 0:
                self.entryFormat = [x for x in L[0]]
            for entry in L:
                if self.add_entry(entry):
                    entryAddCount += 1
        return entryAddCount
        
    def add_dict(self, L):
        """Add entries from a list of dictionaries to the glossary."""
        entryAddCount = 0
        if len(L) > 0:
            if len(self.entryFormat) == 0:
                self.entryFormat = [x for x in L[0].keys()]
            for entry in L:
                if self.add_entry(entry):
                    entryAddCount += 1
        return entryAddCount
    
    def add_entry(self, e):
        """Add given term or entry to glossary.
        
        If a string is given it will be interpreted as a new term, which will
        be added with all other fields left blank.
        If a dict or list is given a new glossary entry will be added.
        For a dict the keys must match the entryFormat.
        For a list the entryFormat will be used to map the list elements.
        If the term/entry to add collides with an existing term/entry an error
        will be raised.
        """
        if isinstance(e, str):
            if e in self.get_terms():
                return False
            else:
                e = e.strip()
                newEntry = {x:'' for x in self.entryFormat}
                newEntry['term'] = e
                self.content.append(newEntry)
                return True
        if isinstance(e, dict):        
            if e['term'] in self.get_terms():
                return False
            else:
                if len(self.entryFormat) == len(e):
                    # Will raise error if dict misses a key in entryFormat.
                    newEntry = {x: e[x] for x in self.entryFormat}
                    self.content.append(newEntry)
                    return True
                else:
                    return False
        if isinstance(e, list):
            if e[self.entryFormat.index('term')] in self.get_terms():
                return False
            else:
                if len(self.entryFormat) == len(e):
                    newEntry = {x: e[self.entryFormat.index(x)]\
                        for x in self.entryFormat}
                    self.content.append(newEntry)
                    return True
                else:
                    return False
        else:
            raise GlossaryError("Invalid argument type.")
        
        return True
        
    def reinit(self, glossary, fmt=None):
        """Reinitialize Glossary object with data given in glossary."""
        return
    
    def reset(self):
        """Drop all glossary entries so an empty Glossary object is left."""
        return
    
    def read_csv(self, filename, dialect=None):
        """Read glossary entries from .csv file using given format."""
        try:
            fd = open(filename, 'r', newline='')
        except Exception as e:
            raise
        
        csvreader = csv.reader(fd, dialect=dialect)
        
        entries = [x for x in csvreader]
        
        self.add_list(entries, entries[0])
        
        if not fd.closed:
            fd.close()
        
        return
    
    def write_csv(self, filename, dialect=None):
        """Save glossary to .csv file using given format."""
        try:
            fd = open(filename, 'w', newline='')
        except Exception as e:
            raise
        
        csvwriter = csv.DictWriter(fd, dialect=dialect)
        csvwriter.writerows(self.content)
        
        if not fd.closed:
            fd.close()
        
        return
        
    def write_html(self, filename, outputFormat=None):
        """Save glossary to .html file."""
        try:
            fd = open(filename, 'w')
        except Exception as e:
            raise
        # TODO
        if not fd.closed:
            fd.close()
        return
        
    def write_latex(self, filename, outputFormat=None):
        """Save glossary to latex file."""
        try:
            fd = open(filename, 'w')
        except Exception as e:
            raise
        # TODO
        if not fd.closed:
            fd.close()
        return
    
    def remove(self, term):
        """Remove given term from glossary."""
        if not isinstance(term, str):
            raise GlossaryError("Invalid argument type.")
        
        term = term.strip()
        if term in self.get_terms():
            self.content.remove()
            entry = [e for e in self.content if e[termIndex] == term]
            self.content.remove
        else:
            self.__notify("Term "+t+" not in glossary. Skipping operation.")
            return False
        return True
    
    def get(self, term):
        """Get the glossary entry of given term."""
        if not isinstance(term, str):
            raise GlossaryError("Invalid argument type.")
        
        term = term.strip()
        if term in self.get_terms():
            entry = [x for x in self.content if x['term'] == term]
            return entry[0]
        else:
            return None
    
    def get_terms(self):
        """Return a list of terms in the glossary."""
        terms = []
        for e in self.content:
            terms.append(e['term'])
        return terms
        
    def set(self, entry):
        """Set the given glossary entry."""
        return

