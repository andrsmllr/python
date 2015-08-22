
class A(object):
  def __init__(self):
    print("A init.")
    
class B1(A):
  def __init__(self):
    super().__init__() # Simplified super() usage.
    print("B1 init.")

class B2(A):
  def __init__(self):
    super(B2, self).__init__() # Explicit super usage.
    print("B2 init.")

class C(object):
  def __init__(self):
    print("C init.")
    
class D1(B1, C):
  def __init__(self):
    super(D1, self).__init__() # This call to super() will call the parent
                              # methods in resolution order, i.e. parent classes
                              # from left to right will be checked for the
                              # requested method, the first one found will be
                              # executed.
    print("D1 init.")
    
class D2(B2, C):
  def __init__(self):
    C.__init__(self) # Here we explicitly select which parents method to call.
    B2.__init__(self)
    print("D2 init.")
