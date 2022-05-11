'''
Created on 16 avr. 2020

@author: ledru
License: MIT
'''

from tkinter import filedialog
from tkinter import *
import ProjectionCSV #import GenerateCSVProjections

root_win=Tk()
root_win.withdraw()
filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
print ("Processing "+filename)

nb=ProjectionCSV.GenerateCSVProjections(filename)  
print("The file was split in "+str(nb)+" testcases!")  
root_win.destroy()