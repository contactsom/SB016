print("START: This is the example of Text File -- *.txt -- Handling")

file=open("simple.txt",'w')
# Open the "simple.txt"
# If "simple.txt" does not exist then Create the file with same name and Type i.e "simple.txt"
# w- Giving the Write permission
print("What is File Name :",file.name)
print("What is File Mode :",file.mode)

print("is File Closed ? :",file.closed)
file.close()
print("is File Closed ? :",file.closed)




