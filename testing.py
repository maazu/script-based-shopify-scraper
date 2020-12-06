import tkinter
from tkinter import *
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
import cv2

from display import *

def testing_urls_page(self,dataset_path):

    print('Testing py =========>',dataset_path)
    cv2.destroyAllWindows()
    #refresh the right side GUI
    self.root.update()

    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)
    rightframe.place(height=800, width=800, x=200, y=0)
    #heading label
    top_heading = Label(rightframe, text="URL Validation Testing", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 20)
    # description label

    #video label

    global validation_name_text_box
    global video_location_text_box


    # Browse_csv_button = Button(rightframe, text="Load dataset", width = 15,command = lambda:open_csv_file_selection_dialogbox(self) )
    # Browse_csv_button.place(x = 625, y = 200)
    #

    next_step_button = Button(rightframe, text=" Next ",width = 15,command = lambda:next_page(self) )
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


def next_page(self):
    if(field_validation()):
        validation_dataset_path = (video_location_text_box.get())
        page_refresh(self,validation_dataset_path)
