print("START: This is the example of Text File -- *.txt -- Handling")

file=open("data.txt",'r') # Read
lines=file.readlines()
for line in lines:
     print(line,end='')

#file.close()








