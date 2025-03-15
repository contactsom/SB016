print("START: This is the example of Text File -- *.txt -- Handling")

file=open("data.txt",'r') # Read

line1=file.readline()
print(line1,end='')

line2=file.readline()
print(line2,end='')

line3=file.readline()
print(line3,end='')

file.close()








