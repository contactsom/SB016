class Student:
  def __init__(self): # In-build Function in python from where execution start
      self.name=""
      self.age=None
      self.salary=6000

  def getDeatils(self):
      print("Hello I am ",self.name)
      print("Hello My Age is ", self.age)
      print("Hello My Salery is ", self.salary)




print(Student.__doc__)
help(Student)


#getDeatils()