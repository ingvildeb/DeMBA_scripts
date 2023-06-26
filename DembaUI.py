#!/usr/bin/python

import tkinter
from tkinter import *  
from tkinter import filedialog

#from new_elastix_code_testing_param_function_examples import runTransform


def my_function():
    print(inp.get())
    
    
    
#    runTransform(
 #       )
    #text.insert(END, "running transformation on volume x and target y... this can take up to xxx minutes")
    
    
def create_func_for_button(path_input_box):
    
    def open_file_func():
        input_filename = filedialog.askopenfilename(title="Choose your input file")
        text.insert(END, f"opened file {input_filename}\n")
        path_input_box.insert(END, input_filename)
        
    return open_file_func
        


def create_entry_widget(labelText = "", buttonText = "Select"):
    label = tkinter.Label(top, text=labelText)
    inp = tkinter.Entry(width = 60)
    button_func = create_func_for_button(inp)
    button = tkinter.Button(top, text = buttonText, command=button_func)  
    
    return label, inp, button

top = tkinter.Tk()
top.title("Demba Warper")
top.geometry("800x800")  
#top.iconphoto(False, PhotoImage(file='Martin.PNG'))

# Code to add widgets will go here...


"""Create entry widgets"""

FixedVolLabel, FixedVolInp, FixedVolButton = create_entry_widget("Fixed Volume")

MovingVolLabel, MovingVolInp, MovingVolButton = create_entry_widget("Moving Volume")

FixedPointsLabel, FixedPointsInp, FixedPointsButton = create_entry_widget("Fixed Points")

MovingPointsLabel, MovingPointsInp, MovingPointsButton = create_entry_widget("Moving Points")

OutputPathLabel, OutputPathInp, OutputPathButton = create_entry_widget("Output Path")
text = tkinter.Text(width=60)

"""Grid placement"""

FixedVolLabel.grid(row=2, column=1, pady = 5)
FixedVolInp.grid(row=2, column=2, pady = 5)
FixedVolButton.grid(row=2, column=3, pady = 5, padx = 5)

MovingVolLabel.grid(row=3, column=1, pady = 5)
MovingVolInp.grid(row=3, column=2, pady = 5)
MovingVolButton.grid(row=3, column=3, pady = 5, padx = 5)

FixedPointsLabel.grid(row=4, column=1, pady = 5)
FixedPointsInp.grid(row=4, column=2, pady = 5)
FixedPointsButton.grid(row=4, column=3, pady = 5, padx = 5)

MovingPointsLabel.grid(row=5, column=1, pady = 5)
MovingPointsInp.grid(row=5, column=2, pady = 5)
MovingPointsButton.grid(row=5, column=3, pady = 5, padx = 5)

OutputPathLabel.grid(row=6, column=1, pady = 5)
OutputPathInp.grid(row=6, column=2, pady = 5)
OutputPathButton.grid(row=6, column=3, pady = 5, padx = 5)

text.grid(row=7,column=1, columnspan=3)


#text = Text(top, height=30)
#text.grid(row=6)

top.mainloop()
