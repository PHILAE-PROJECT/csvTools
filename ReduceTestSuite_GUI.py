'''
Created on 16 avr. 2020

@author: ledru
License: MIT
'''
from tkinter import filedialog
from tkinter import *
from ReduceTestSuite import *
from ExecuteTraceOpti import *



#import ExecuteTraceOpti 

init_dir = "."


def execute_traces():
    if opti_value.get() == 0:
        opti = False
    else:
        opti = True
    filePath = fnameReduced.get()
    if len(filePath) > 0 and (os.path.isdir(filePath) or os.path.isfile(filePath)):
        print("Executing on "+filePath+" optimode = "+str(opti))
        executeTraceOnMutants(filePath,opti)
    else:
        print("Entry is empty or invalid path. Choose a file or directory")


def reduce_testsuite():
  
    subsume = subsumption_value.get()
    absFunc = opt_variable.get()
    dirPath = fname.get()
    if len(dirPath) > 0 and os.path.isdir(dirPath):
        print("Reducing "+fname.get())
        print(" absFunction = "+absFunc)
        ComputeSigDictAndReduce(dirPath,absFunc,subsume,"")
        if subsume== 1:
            suffix="_sub"
        elif subsume == 2:
            suffix="_su2"
        else:
            suffix=""
        fnameReduced.set(os.path.join(dirPath,"reducedTS-"+absFunc+suffix))
        win_button_exec.config(state='normal')
    else:
        print("Entry is empty or invalid path. Choose a directory")

def exit_window():
    exit()

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
my_window.geometry("1000x400")
my_window.title("Cluster and reduce a test suite")
win_title=Label(my_window,text="Test suite clustering, reduction, and evaluation",font=("arial",16,"bold"))
win_title.pack()

file_label = Label(my_window,text="Directory where the test suite is stored")
file_label.place(x=20,y=50)

fname=StringVar()
win_file_entry=Entry(my_window,textvar=fname,width=160)
win_file_entry.place(x=20,y=80)

file2_label = Label(my_window,text="Directory where the reduced test suite is stored")
file2_label.place(x=20,y=200)

fnameReduced=StringVar()
win_TS_entry=Entry(my_window,textvar=fnameReduced,width=160,state='readonly')
win_TS_entry.place(x=20,y=230)

absFunc_label = Label(my_window,text="Abstraction function: ")
absFunc_label.place(x=20,y=125)

option_list = [
    "OpNames_Set",
    "OpNamesAndRet_Set",
    "OpNamesAndAbsRet_Set",
    "OpNames_Bag",
    "OpNamesAndRet_Bag",
    "OpNamesAndAbsRet_Bag",
    "OpNames_Seq",
    "OpNamesAndRet_Seq",
    "OpNamesAndAbsRet_Seq",
    "OpNames_Seq_NoSt",
    "OpNamesAndRet_Seq_NoSt",
    "OpNamesAndAbsRet_Seq_NoSt"
] 
opt_variable = StringVar()
opt_variable.set(option_list[0])
optionmenu_widget = OptionMenu(my_window,opt_variable, *option_list)
optionmenu_widget.place(x=150,y=120)

subsume_label = Label(my_window,text="Subsumption : ")
subsume_label.place(x=400,y=125)

subsumption_value = IntVar()
subsumption_value.set(0)
#subsumption_button = Checkbutton(my_window, text="with subsumption",variable=subsumption_value)
#subsumption_button.place(x=400,y=120)
subsumption_button0 = Radiobutton(my_window, text="0: No subsumption", padx = 20, variable=subsumption_value, value=0).place(x=500,y=125)
subsumption_button1 = Radiobutton(my_window, text="1: subset, subbag, prefix", padx = 20, variable=subsumption_value, value=1).place(x=500,y=150)
subsumption_button2 = Radiobutton(my_window, text="2: (subset,subbag), matchedBy", padx = 20, variable=subsumption_value, value=2).place(x=500,y=175)

opti_value = IntVar()
opti_value.set(1)
optiMode_button = Checkbutton(my_window, text="Optimized mode",variable=opti_value)
optiMode_button.place(x=50,y=270)

win_button_dir = Button(my_window,text="1. Select directory",command=ask_for_dir)
win_button_dir.place(x=860,y=45)

win_button_reduce = Button(my_window,text="2. Reduce",command=reduce_testsuite)
win_button_reduce.place(x=900,y=120)

win_button_exec = Button(my_window,text="3. Execute Reduced Test Suite",command=execute_traces,state='disabled')
win_button_exec.place(x=800,y=270)

win_button_quit = Button(my_window,text="4. Quit",command=exit_window)
win_button_quit.place(x=920,y=350)


my_window.mainloop()
