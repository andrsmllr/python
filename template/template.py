#!/bin/python
##############################################################################
"""
Module docstring.
"""

def function():
    """Function docstring."""
    print("Function called.")

class Class(object):
    """Class docstring."""
    publicClassAttribute = 1
    _privateClassAttribute = 2
    def _privateClassMethod():
        """Private class method docstring."""
        print("Private class method called.")
    def publicClassMethod():
        """Public class method docstring."""
        print("Public class method called.")
    def __init__(self):
        """Init docstring."""
        print("Init called.")
        publicAttribute = 3
        _privateAttribute = 4
    def publicMethod(self):
        """Public method docstring."""
        print("Public method called.")
    def _privateMethod(self):
        """Private method docstring."""
        print("Private method called.")
        
if __name__ == '__main__':
    print("template.py called as script.")

