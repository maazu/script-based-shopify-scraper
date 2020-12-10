
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 18:20:51 2020

@author: Maaz
"""
import time 
import os
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
from tkinter import ttk 
import pandas as pd
from product_count import *
from threading import Thread
from tkinter import messagebox as mbox

standard_font_name = "Motiva Sans"
rightframe_background_color = "#EDE9D8"
foreground_color = "#173630"
font_weight ="bold"
button_background_color = "#108043"
text_font_size = 12
def read_csv_file(csv_file_path):
    df =  pd.read_csv(csv_file_path, index_col=False)
    df_columns =tuple(df.columns)
   
    return df_columns


def pre_sort_dataset(self,page_name):
    
    self.root.update()
    global rightframe
    rightframe = Frame(self.root,bg =  rightframe_background_color)  
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    
    page_heading = Label(rightframe, text="Sort Dataset", font=(standard_font_name, 16,font_weight),bg =rightframe_background_color,fg = foreground_color)
    page_heading.place(x=35, y=20)
 
    page_note = "Select the dataset you would like to sort according to their total store products range."
    page_note = Label(rightframe, text = page_note, font = (standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color)
    page_note.place(x=35, y=60)
    


    processing_type_label_name = Label(rightframe, text="Name", font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color)
    processing_type_label_name.place(x=35, y = 100)
    
    
    global processing_type_text_box #name textbox
    processing_type_text_box = Entry(rightframe)
    processing_type_text_box.place(x = 135, y = 100,width = 590)  
  
    
   
    processing_dataset_location_label = Label(rightframe, text="Path", font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color)
    processing_dataset_location_label.place(x=35, y = 150)
    
    
    global processing_dataset_location_text_box #path textbox
    processing_dataset_location_text_box = Entry(rightframe)
    processing_dataset_location_text_box.place(x = 135, y = 150,width = 590)  
 
    
    Browse_csv_button = Button(rightframe, text="Load dataset", width = 15,command = lambda:open_dialog_box_csv(self) )
    Browse_csv_button.place(x = 610, y = 200)
 
    
    global column_selection_label
    column_selection_note = " Please select the column name which contains the main url and store url column"
    column_selection_label =  Label(rightframe, text = column_selection_note ,  font=(standard_font_name, text_font_size,font_weight), bg =rightframe_background_color,fg = foreground_color)
    
  
   
    global column_url_label_one, column_url_label_two
   
    column_url_label_one = Label(rightframe, text="Main url column", font=(standard_font_name, text_font_size,font_weight) , bg =rightframe_background_color,fg = foreground_color) 
    column_url_label_two = Label(rightframe, text="Store url column", font=(standard_font_name, text_font_size,font_weight), bg =rightframe_background_color,fg = foreground_color) 
    
   
   
    
   
def field_validation():
    if(processing_type_text_box.get() == ''):
        mbox.showerror("Missing Dataset Name","Dataset Name Missing")
        return False
    elif(processing_dataset_location_text_box.get() == ''):
        mbox.showerror("Missing File Path","Dataset file path is missing")
        return False
    return True



def open_dialog_box_csv(self):
       
        if(processing_type_text_box.get() == ''):
             mbox.showerror("Missing Dataset Name","Dataset Name Missing")
        
        else:   
            full_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file", filetypes=[("CSV (Comma separated file)", "*.csv")]) # select a video file from the hard drive
            if ( full_file_path != ''):
              
                 processing_dataset_location_text_box.config(state=NORMAL)
                 processing_dataset_location_text_box.delete(0,END)
                 processing_dataset_location_text_box.insert(0,full_file_path)
                 processing_dataset_location_text_box.config(state=DISABLED)
                 processing_type_text_box.config(state=DISABLED)
                 
                 if (field_validation()): # Adding combobox drop down list
                       
                        loaded_dataset_name = processing_type_text_box.get()
                        loaded_dataset_path = processing_dataset_location_text_box.get()
                        
                        column_selection_label.place(x = 35, y = 250)
                        
                        column_url_label_one.place(x = 35, y = 300)
                        column_url_label_two.place(x = 35,y = 350)
                       
                        column_one_option_menu = ttk.Combobox(rightframe,  values = (read_csv_file(loaded_dataset_path)),state="readonly", width = 27) 
                        column_two_option_menu = ttk.Combobox(rightframe,  values = (read_csv_file(loaded_dataset_path)), state="readonly",width = 27) 
                        
                        column_one_option_menu.place(x = 185, y = 300)
                        
                        column_two_option_menu.place(x = 185, y = 350)
                       
                      
                   
                        sort_step_button = Button(rightframe, text="Sort Dataset", width = 15,command = lambda:start_reformatting(self,loaded_dataset_path,column_one_option_menu.get(), column_two_option_menu.get()) )
    
                        sort_step_button.place(x = 610, y = 500)
                        sort_step_button.pack_forget()
                       
                       
                        
                        
  
    
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        #print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
 

                        
def save_reformatted_data(df):
    save_data_set_path = filedialog.askdirectory (initialdir="/", title="Select a directory", ) # select a video file from the hard drive
    if ( save_data_set_path != ''):
        save_thread = ThreadWithReturnValue(target = save_reformatted_df, args = (df,save_data_set_path))
        save_thread.start()
        confirmation = save_thread.join()   
        mbox.showinfo("Information", confirmation)
        rightframe.pack()
   
   

def start_reformatting(self,loaded_dataset_path,main_urls,store_urls):
   
    if(field_validation()):
        
        products_counting_gui_update(self,loaded_dataset_path,main_urls,store_urls)
        

      