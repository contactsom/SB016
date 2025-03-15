print("START: This is the example of Text File -- *.txt -- Handling")

#file=open("abc.txt",'w')

file=open("mylist.txt",'a') # Append
mylist = ["A \n","B \n","C \n","D \n","E \n","F \n"]

file.writelines(mylist)

file.close()








