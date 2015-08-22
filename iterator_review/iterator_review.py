#!/bin/python

class MyIterator(object):
  def __init__(self, word):
    self.pos = 0
    if isinstance(word, str):
      self.word = word
    else:
      self.word = "None"
    
  def __iter__(self):
    """Return the iterator object, implicitly called at the start of loops."""
    self.pos = 0
    return self # A different object/class could be returned.
                # We use self here for simplicity.
    
  def __next__(self):
    """Return the next value each time __next__() is called."""
    if self.pos >= len(self.word):
      raise StopIteration # When done, StopIteration must be raised.
    else:
      w = self.word[self.pos]
      self.pos += 1
      return w # Return next value.

if __name__ == '__main__':
  # Create iterator.
  m = MyIterator("foobar")
  
  # Use it.
  for c in m:
    print(c)
