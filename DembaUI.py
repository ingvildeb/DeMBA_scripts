#!/usr/bin/python

import tkinter
from tkinter import *  
from tkinter import filedialog
from tkinter.messagebox import showinfo
import DeMBA_functions as dfs
import os


#from new_elastix_code_testing_param_function_examples import runTransform
import threading

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
        


def create_entry_widget(labelText = "", buttonText = "Select", stringvar = ""):
    label = tkinter.Label(top, text=labelText)
    inp = tkinter.Entry(width = 100, textvariable=stringvar)
    button_func = create_func_for_button(inp)
    button = tkinter.Button(top, text = buttonText, command=button_func)
    
    return label, inp, button



top = tkinter.Tk()
top.title("Demba Warper")
top.geometry("800x800")  
#top.iconphoto(False, PhotoImage(file='Martin.PNG'))


fixedVol = tkinter.StringVar()
movingVol = tkinter.StringVar()
pointsFile = tkinter.StringVar()
movingSegmentation = tkinter.StringVar()


fixedAge = tkinter.StringVar()
movingAge = tkinter.StringVar()
runName = tkinter.StringVar()



def runButton_clicked():
    """ callback when the run button is clicked
    """
    
    fixedVolPath = fixedVol.get()
    movingVolPath = movingVol.get()
    pointsFilePath = pointsFile.get()
    movingSegmentationPath = movingSegmentation.get()
    
    fixedAgeString = fixedAge.get()
    movingAgeString = movingAge.get()
    runNameString = runName.get()
    
    workingDirPath = os.path.dirname(pointsFilePath) + "//"
    
    nl = '\n'
    text.insert(END, f'{nl}the working path is {workingDirPath}...')
    
    text.insert(END, f'{nl}running script on {pointsFilePath}...')
    
    fixedPointsPath, movingPointsPath = dfs.LMRtoElastixPoints(pointsFilePath, fixedAgeString, movingAgeString)
    
    text.insert(END, f'{nl}{nl}done converting LMR points')
    
    text.insert(END, f'{nl}running transform...{nl}This can take up to 20 minutes')
    
    text.insert(END, f'{nl}the movingSegmentation is {movingSegmentationPath}')
    
    thread = threading.Thread(target=dfs.runTransform, args=(fixedVolPath, movingVolPath, fixedPointsPath, movingPointsPath, movingSegmentationPath, 
                                                              workingDirPath + runNameString + "_resultTemplate.nii", workingDirPath + runNameString + "_resultSegmentation.nii"))
    thread.start()
    
    # text.insert(END, f'Finished the registration!')
    



# Code to add widgets will go here...


"""Create entry widgets"""

fixedVolLabel, fixedVolInp, fixedVolButton = create_entry_widget(labelText = "Fixed volume", stringvar = fixedVol)

movingVolLabel, movingVolInp, movingVolButton = create_entry_widget("Moving volume", stringvar = movingVol)

pointsLabel, pointsInp, pointsButton = create_entry_widget("LMR points file", stringvar = pointsFile)

movingSegmentationLabel, movingSegmentationInp, movingSegmentationButton = create_entry_widget("Moving segmentation", stringvar = movingSegmentation)

fixedAgeLabel = tkinter.Label(text = "Fixed volume age")
fixedAgeInp = tkinter.Entry(width = 30, textvariable=fixedAge)

movingAgeLabel = tkinter.Label(text = "Moving volume age")
movingAgeInp = tkinter.Entry(width = 30, textvariable=movingAge)

runNameLabel = tkinter.Label(text = "Run name")
runNameInp = tkinter.Entry(width = 30, textvariable=runName)

text = tkinter.Text(width=60)

runButton = tkinter.Button(text = "Run volume :D", command=runButton_clicked)

"""Grid placement"""

fixedAgeLabel.grid(row=2, column=1, pady = 5)
fixedAgeInp.grid(row=2, column=2, pady = 5)

movingAgeLabel.grid(row=3, column=1, pady = 5)
movingAgeInp.grid(row=3, column=2, pady = 5)

fixedVolLabel.grid(row=4, column=1, pady = 5)
fixedVolInp.grid(row=4, column=2, pady = 5)
fixedVolButton.grid(row=4, column=3, pady = 5, padx = 5)

movingVolLabel.grid(row=5, column=1, pady = 5)
movingVolInp.grid(row=5, column=2, pady = 5)
movingVolButton.grid(row=5, column=3, pady = 5, padx = 5)

pointsLabel.grid(row=6, column=1, pady = 5)
pointsInp.grid(row=6, column=2, pady = 5)
pointsButton.grid(row=6, column=3, pady = 5, padx = 5)

movingSegmentationLabel.grid(row=7, column=1, pady = 5)
movingSegmentationInp.grid(row=7, column=2, pady = 5)
movingSegmentationButton.grid(row=7, column=3, pady = 5, padx = 5)

runNameLabel.grid(row=8, column=1, pady = 5)
runNameInp.grid(row=8, column=2, pady = 5)


text.grid(row=9,column=1, columnspan=3)

runButton.grid(row=10,column=1,columnspan=3)




#text = Text(top, height=30)
#text.grid(row=6)

top.mainloop()
