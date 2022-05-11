'''
Created on 16 avr. 2020

@author: ledru
License: MIT
'''
from tkinter import filedialog
from tkinter import *
from UniqueObjects import *

init_dir = "."

def makeUnique():
    if singleFile_value.get() == 0:
        singleFileBool = False
    else:
        singleFileBool = True
    filePath = fname.get()
    if len(filePath) > 0 and (os.path.isdir(filePath) or os.path.isfile(filePath)):
        MakeUniqueObjects(filePath,singleFileBool)
    else:
        print("Entry is empty or invalid path. Choose a file or directory")
    print("Processed!")
    
def exit_window():
    exit()
    
def ask_for_file():
    global init_dir
    if os.path.isdir(fname.get()):
        init_dir = fname.get()
    elif os.path.isfile(fname.get()):
        init_dir = os.path.dirname(fname.get())
    filename =  filedialog.askopenfilename(initialdir = init_dir,title = "Select csv file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    if filename != "":
        fname.set(filename)
        init_dir=os.path.dirname(filename)
    singleFile_value.set(0)

def ask_for_dir():
    global init_dir
    if os.path.isdir(fname.get()):
        init_dir = fname.get()
    elif os.path.isfile(fname.get()):
        init_dir = os.path.dirname(fname.get())

    dirname =  filedialog.askdirectory(initialdir = init_dir,title = "Select directory")
    if dirname != "":
        fname.set(dirname)
        init_dir=dirname

my_window = Tk()
my_window.geometry("800x200")
my_window.title("Use Unique Object Identifiers")
win_title=Label(my_window,text="Use Unique Object Identifiers",font=("arial",16,"bold"))
win_title.pack()

fname=StringVar()

win_file_entry=Entry(my_window,textvar=fname,width=120)
win_file_entry.place(x=20,y=80)

or_label = Label(my_window,text="Click on one of the select buttons:")
or_label.place(x=350,y=50)

file_label = Label(my_window,text="Target file or directory")
file_label.place(x=20,y=50)

win_button_file = Button(my_window,text="Select csv file",command=ask_for_file)
win_button_file.place(x=550,y=45)

win_button_dir = Button(my_window,text="Select directory",command=ask_for_dir)
win_button_dir.place(x=640,y=45)


singleFile_value = IntVar()
singleFile_value.set(1)
optiMode_button = Checkbutton(my_window, text="Put results in a single csv file",variable=singleFile_value)
optiMode_button.place(x=50,y=120)

win_button_exec = Button(my_window,text="Make Unique",command=makeUnique)
win_button_exec.place(x=600,y=150)

win_button_quit = Button(my_window,text="Quit",command=exit_window)
win_button_quit.place(x=700,y=150)

#filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
#print (filename)

my_window.mainloop()
