class Student:
  def __init__(self): # In-build Function in python from where execution/initialization start
      self.a = 10
      self.b = 20
      self.c = 30
      self.d = 40
      self.e = 50
      self.f = 60
      self.g = 70
      self.h = 80


  def getDeatils(self):
      print("Value of a ", self.a)
      print("Value of b ", self.b)
      print("Value of c ", self.c)
      print("Value of d ", self.d)
      print("Value of e ", self.e)
      print("Value of f ", self.f)
      print("Value of g ", self.g)
      print("Value of h ", self.h)



stuobject=Student()
stuobject.getDeatils()
print(stuobject.__dict__)
