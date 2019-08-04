import sys
import os
from tkinter import *


top = Tk()

def adduser():
    os.system('python add_user.py')

def deleteuser():
    os.system('python delete_user.py')

def recognize():
    os.system('python recognize.py')

def mictest():
    os.system('python test.py')

def audiofile():
    os.system('python audioinput3.py')

com1 = Button(top, text="Add User",command = adduser)
com1.pack()

com2 = Button(top, text="Delete User",command = deleteuser)
com2.pack()

com3 = Button(top, text="Recognize",command = recognize)
com3.pack()

com4 = Button(top, text="Input from mic",command = mictest)
com4.pack()

com5 = Button(top, text="Input from audio file",command = audiofile)
com5.pack()

top.mainloop()