from threading import *

def currentThread():
    for i in range(1,6):
        print("**** Hello i am child Thread ")

t=Thread(target=currentThread)
t.start()