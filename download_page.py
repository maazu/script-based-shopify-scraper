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
from reformat_store_urls import *
from threading import Thread
from tkinter import messagebox as mbox
from validate_urls import *
from threading import Thread
from download_products import *


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


def download_csv_from_dataset(self,page_name):
    
    self.root.update()
    global rightframe
    rightframe = Frame(self.root,bg =  rightframe_background_color)  
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    
    page_heading = Label(rightframe, text="Download Products Data From Shopify Store", font=(standard_font_name, 16,font_weight),bg =rightframe_background_color,fg = foreground_color)
    page_heading.place(x=35, y=20)
 
    page_note = "Select the dataset you would like to Download."
    page_note = Label(rightframe, text = page_note, font = (standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color)
    page_note.place(x=35, y=60)
    
   
    processing_dataset_location_label = Label(rightframe, text="Path", font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color)
    processing_dataset_location_label.place(x=35, y = 150)
    
    
    global processing_dataset_location_text_box #path textbox
    processing_dataset_location_text_box = Entry(rightframe)
    processing_dataset_location_text_box.place(x = 135, y = 150,width = 590)  
 
   
    
    
    global Browse_csv_button #path textbox
   
 
    Browse_csv_button = Button(rightframe, text="Load dataset", width = 15,command = lambda:open_dialog_box_csv(self) )
    Browse_csv_button.place(x = 610, y = 200)
 
    
    global column_selection_label
    column_selection_note = " Please select the column name which contains the main url and store url column"
    column_selection_label =  Label(rightframe, text = column_selection_note ,  font=(standard_font_name, text_font_size,font_weight), bg =rightframe_background_color,fg = foreground_color)
    
  
   
    global column_url_label_one, column_url_label_two
   
    column_url_label_one = Label(rightframe, text="Main url column", font=(standard_font_name, text_font_size,font_weight) , bg =rightframe_background_color,fg = foreground_color) 
    column_url_label_two = Label(rightframe, text="Store url column", font=(standard_font_name, text_font_size,font_weight), bg =rightframe_background_color,fg = foreground_color) 
    
   
   
    
   
def field_validation():
    if(processing_dataset_location_text_box.get() == ''):
        mbox.showerror("Missing File Path","Dataset file path is missing")
        return False
    else:
        return True


def get_download_directory(self,loaded_dataset_path,column_one_option_menu, column_two_option_menu):
     dowload_file_path = filedialog.askdirectory(initialdir="/", title="Select a Download Folder" ) 
     if ( dowload_file_path != ''):
         processing_dataset_file_saving_location.config(state=NORMAL)
         processing_dataset_file_saving_location.delete(0,END)
         processing_dataset_file_saving_location.insert(0,dowload_file_path)
         processing_dataset_file_saving_location.config(state=DISABLED)
         processing_dataset_file_saving_location.config(state=DISABLED)
         
         downloading_step_button = Button(rightframe, text="Start Downloading", width = 15,command = lambda:downlad_data_from_gui_update(self,dowload_file_path,loaded_dataset_path,column_one_option_menu, column_two_option_menu))
         downloading_step_button.place(x = 610, y = 600)
         downloading_step_button.pack_forget()
                       

def open_dialog_box_csv(self):
          
            full_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file", filetypes=[("CSV (Comma separated file)", "*.csv")]) # select a video file from the hard drive
            if ( full_file_path != ''):
               
                 processing_dataset_location_text_box.config(state=NORMAL)
                 processing_dataset_location_text_box.delete(0,END)
                 processing_dataset_location_text_box.insert(0,full_file_path)
                 processing_dataset_location_text_box.config(state=DISABLED)
                 
                 
                 if (field_validation()): # Adding combobox drop down list
                       
                     
                        loaded_dataset_path = processing_dataset_location_text_box.get()
                        
                        column_selection_label.place(x = 35, y = 250)
                        
                        column_url_label_one.place(x = 35, y = 300)
                        column_url_label_two.place(x = 35,y = 350)
                       
                        column_one_option_menu = ttk.Combobox(rightframe,  values = (read_csv_file(loaded_dataset_path)),state="readonly", width = 27) 
                        column_two_option_menu = ttk.Combobox(rightframe,  values = (read_csv_file(loaded_dataset_path)), state="readonly",width = 27) 
                        
                        column_one_option_menu.place(x = 185, y = 300)
                        
                        column_two_option_menu.place(x = 185, y = 350)
                       
                        global processing_dataset_file_saving_location
                        processing_dataset_file_saving_location_label = Label(rightframe, text="Download Path", font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color)
                        processing_dataset_file_saving_location_label.place(x=35, y = 400)
       
                        processing_dataset_file_saving_location = Entry(rightframe)
                        processing_dataset_file_saving_location.place(x = 35, y = 450,width = 590)  
                     
                        note_2 = "Note: This is the path where you would like to save the csv files extracted from each shopify store."
                        note_2 = Label(rightframe, text=note_2, font=(standard_font_name, 8,font_weight),bg =rightframe_background_color,fg = foreground_color)
                        note_2.place(x=35, y = 490)
                       
                        downlaode_csv_path_button = Button(rightframe, text="Download Path", width = 15,command = lambda:get_download_directory(self,loaded_dataset_path,column_one_option_menu.get(), column_two_option_menu.get())) 
                        downlaode_csv_path_button.place(x = 650, y = 450)    
                       
                       
                        
                        
  
    
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
   
   

def start_validation(self,loaded_dataset_path,main_urls,store_urls):
   
    if (field_validation()):
        
        products_downloading_gui_update(self,loaded_dataset_path,main_urls,store_urls)
        
        #save_step_button = Button(rightframe, text="Finish & Save CSV",  bg= button_background_color,fg="WHITE", width = 15,command = lambda:save_reformatted_data(df) )
        #save_step_button.place(x = 610, y = 500)