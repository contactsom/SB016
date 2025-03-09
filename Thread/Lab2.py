from threading import *

def currentThread():
    for i in range(1,6):
        print("***** Hello I am Child Thread ")

t=Thread(target=currentThread()) # Creatinmg the Thread, I am assigning a task [currentThread] to the thread t.
t.start() # Starting the Thread

for i in range(1,5):
    print("******* Hello I am Main Thread")
