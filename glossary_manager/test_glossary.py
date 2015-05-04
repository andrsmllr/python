#!/bin/python

import unittest
import glossary

class TestGlossary(unittest.TestCase):
    """Unit testing of class Glossary."""
    def setUp(self):
        """Initialize test fixture."""
        self.g = glossary.Glossary()
        
    def tearDown(self):
        """Deinitialize test fixture."""
        pass
        
    def test_createEmptyGlossay(self):
        """Test constructor of class Glossary."""
        self.assertIsInstance(self.g, glossary.Glossary)
        
    def test_createGlossaryByList(self):
        """Test constructor of class Glossary when passing over a list."""
        li = []
        li.append(['term', 'tags', 'value'])
        li.append(['foo', 'a', '1'])
        li.append(['bar', 'a, b', '2'])
        li.append(['gnark', 'a, c', '3'])
        self.g = glossary.Glossary(li)
        
    def test_addList(self):
        """Test to update a Glossary instance with a list."""
        lili = []
        lili.append(['term', 'tags', 'value'])
        lili.append(['foo', 'a', '1'])
        lili.append(['bar', 'a, b', '2'])
        lili.append(['gnark', 'a, c', '3'])
        self.g.add_list(lili)
        
    def test_addDict(self):
        """Test to update a Glossary instance with a dict."""
        lidi = []
        lidi.append({'term': 'foo', 'tags': 'a', 'value': '1'})
        lidi.append({'term': 'bar', 'tags': 'a, b', 'value': '2'})
        lidi.append({'term': 'gnark', 'tags': 'a, c', 'value': '3'})
        self.g.add_dict(lidi)
        
    def test_addEntryByString(self):
        """Test to add a new entry to a Glossary instance by string."""
        b = self.g.add_entry('foo')
        self.assertTrue(b)
        
    def test_addEntryByList(self):
        """Test to add a new entry to a Glossary instance by list."""
        self.g.entryFormat = ['term', 'tags', 'value']
        b = self.g.add_entry(['foo', 'a', '1'])
        self.assertTrue(b)
        
    def test_addEntryByDict(self):
        """Test to add a new entry to a Glossary instance by dict."""
        self.g.entryFormat = ['term', 'tags', 'value']
        b = self.g.add_entry({'term': 'foo', 'tags': 'a', 'value': '1'})
        self.assertTrue(b)
        
    def test_getEntryByTerm(self):
        """Test to retrieve a entry from a Glossary instance."""
        self.g.entryFormat = ['term', 'tags', 'value']
        origEntry = {'term': 'foo', 'tags': 'a', 'value': '1'}
        b = self.g.add_entry(origEntry)
        self.assertTrue(b)
        retrievedEntry = self.g.get(origEntry['term'])
        self.assertEqual(retrievedEntry, origEntry)
    
    def test_removeEntryByTerm(self):
        pass
    
    def test_getTerms(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()

