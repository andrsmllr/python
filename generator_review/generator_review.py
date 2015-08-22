
def my_generator(word):
  pos = 0
  while len(word) > pos:
    yield word[pos]
    pos += 1

if __name__ == '__main__':
  for c in my_generator("foobar"):
    print("In the generator...")
    print(c)
