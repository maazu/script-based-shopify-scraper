import tkinter
from tkinter import *
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
import cv2



def validation_urls_page(self):
    cv2.destroyAllWindows()  
    #refresh the right side GUI
    self.root.update()
    
    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    #heading label
    top_heading = Label(rightframe, text="URL Validation", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 20)
    # description label
    desc_label = Label(rightframe, text="Please select the validation csv file path.\n ", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    desc_label.place(x=10, y = 58)
 
    #video label
    validation_label = Label(rightframe, text="Validation ID/ Unique Name", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    validation_label.place(x=10, y = 120)

    global validation_name_text_box 
    validation_name_text_box = Entry(rightframe)
    validation_name_text_box.place(x = 150, y = 120,width = 590)  

    validation_location_label = Label(rightframe, text="Dataset Location", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    validation_location_label.place(x=10, y = 160)
   
    global video_location_text_box
    validation_location_text_box = Entry(rightframe)
    validation_location_text_box.place(x = 150, y = 160,width = 590)  


    Browse_csv_button = Button(rightframe, text="Load dataset", width = 15,command = lambda:open_csv_file_selection_dialogbox(self) )
    Browse_csv_button.place(x = 625, y = 200)


    next_step_button = Button(rightframe, text=" Next ",width = 15,command = lambda:validate_urls(self) )
    next_step_button.place(x = 625, y = 600)
    

    

# Open a video file
def open_csv_file_selection_dialogbox(self):
        fullfilename = filedialog.askopenfilename(initialdir="//Gui", title="Select a csv file", filetypes=[("csv file", "*.csv")]) # select a video file from the hard drive
        if(fullfilename != ''):
             validation_name_text_box.delete(0,END)
             validation_name_text_box.insert(0,fullfilename)
      
    

def field_validation():
    if(validation_name_text_box.get() == ''):
        mbox.showerror("csv file Name","Route Name Missing")
        return False
    elif(validation_location_text_box.get() == ''):
        mbox.showerror("Missing File Path","csv path is missing")
        return False
    return True




