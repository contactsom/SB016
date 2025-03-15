class Student:
  def __init__(self): # In-build Function in python from where execution start
      self.name="Rabie"
      self.age=23
      self.salary=5000

  def getDeatils(self):
      print("Hello I am ",self.name)
      print("Hello My Age is ", self.age)
      print("Hello My Salery is ", self.salary)


# 1 Where is getDeatils function  - Inside the Class Student
# 2. Get the Permission from the Class "Student"
# 3. How to get the permission, Create the Object
# 4. How to create the Object objectName=ClassName()

stuobject=Student()
stuobject.getDeatils()
