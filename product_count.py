# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 23:25:13 2020

@author: Maaz
"""
import os
import pandas as pd
import asyncio
import aiohttp
from aiohttp import ClientSession, ClientConnectorError
from datetime import datetime
import time
import tkinter
from tkinter import ttk 
from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename
import threading
import requests 
startTime = datetime.now()
lock = threading.Lock()

counter = 66600
running = False
counted_product = {}
invalid_url = {}
gui_text_area_updates = []


standard_font_name = "Motiva Sans"
rightframe_background_color = "#EDE9D8"
foreground_color = "#173630"
font_weight ="bold"
button_background_color = "#108043"
text_font_size = 12
startTime = datetime.now()

error =[]
pre_sort_data_dict = {}

process_sorting_thread_list = []

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
 





def counter_label(label):  
    def count():  
        if running:  
            global counter  
    
            # To manage the intial delay.  
            if counter==66600:              
                display="Starting..."
            else: 
                tt = datetime.fromtimestamp(counter) 
                
                string = "Total elapsed time: "+   str(datetime.now() - startTime)[:-4] +""
                display=string  
    
            label['text']=display   # Or label.config(text=display)  
    
            # label.after(arg1, arg2) delays by   
            # first argument given in milliseconds  
            # and then calls the function given as second argument.  
            # Generally like here we need to call the   
            # function in which it is present repeatedly.  
            # Delays by 1000ms=1 seconds and call count again.  
            label.after(1000, count)   
            counter += 1
    
    # Triggering the start of the counter.  
    count()       
    
def Start(label):  
    global running  
    running=True
    counter_label(label)  

    
def Stop():  
    global running  
   
    running = False
    


    
def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


def create_shopify_api_endpoint_for_store(url):
    url = "https://" + url + "/products.json?limit=250&page="  
    return url


def create_shopify_api_endpoint_for_store_with_www(url):
    url = "https://www." + url + "/products.json?limit=250&page="  
    return url

def create_shopify_api_endpoint_for_store_with_http(url):
    url = "http://" + url + "/products.json?limit=250&page="  
    return url
    




                        
def save_df_to_selected_path(user_selected_path):
   
    valid_df = pd.DataFrame(list(valid_url.items()),columns = ['Valid store','host']) 
    
    valid_df.to_csv(user_selected_path +"/"+ "sorted-urls-"+ generated_time() +".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
    
    invalid_df = pd.DataFrame(list(invalid_url.items()),columns = ['Invalid store','host']).dropna()
    
    invalid_df.to_csv(user_selected_path+"/"+ "error-sorted-urls-"+ generated_time() +".csv", index=False, line_terminator='\n', encoding ="utf-8-sig")



def save_validated_data():
    save_data_set_path = filedialog.askdirectory (initialdir="/", title="Select a directory", ) # select a video file from the hard drive
    if ( save_data_set_path != ''):
        save_thread = threading.Thread(target=save_df_to_selected_path, args=(save_data_set_path,), daemon=True)  
        save_thread.start()
        confirmation = "Valid and invalid csv file has been saved sucessfully"
        mbox.showinfo("Information", confirmation)
        save_thread.join()








def text_area_statement(count,store,product_range):
    
    gui_text_area.insert(END,("{}\t\t {}\t {}\t\t {}\t\t ".format(count,"Found",product_range,store)+'\n'))
    gui_text_area.update()
    
  


def get_store_data(dataset_path,host_col_name,store_col_name):
    
  df = pd.read_csv(dataset_path,index_col=False).drop_duplicates(keep='first').dropna()
  total_urls = len(list(df[store_col_name]))
  host_name_list = list(df[host_col_name])
  store_list = list(df[store_col_name])
  
  return [total_urls,host_name_list,store_list ]   




def products_counting_gui_update(self,loaded_dataset_path,main_urls,store_urls):
    
    self.root.update()
    global rightframe
    rightframe = Frame(self.root,bg =  rightframe_background_color)  
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    
    global elapsed_time
    elapsed_time = Label(rightframe, text="", font=(standard_font_name, 20,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")  
    elapsed_time.place(x = 180, y = 650)
    
    Start(elapsed_time)
  
    global gui_text_area
    gui_text_area = tkinter.Text(rightframe) 
    gui_text_area.place(x=55, y=60)
    
   
    global get_data_details
    get_data_details = get_store_data(loaded_dataset_path,main_urls,store_urls)
   
    global detected_total_urls
    detected_total_urls  = str(get_data_details[0])
    
    global host_name_list
    host_name_list  = get_data_details[1]
    
    global store_name_list
    store_name_list = get_data_details[2]
   
    
    gui_text_area = tkinter.Text(rightframe) 
    gui_text_area.place(x=55, y=60)
    
    total_url_label = Label(rightframe, text= "\n"+ detected_total_urls +"\n\n\tTotal Urls \t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    total_url_label.place(x=25, y=500)
   
    global valid_urls
    valid_urls = Label(rightframe, text= "\n"+str(len(pre_sort_data_dict)) +"\n\n\tCounted \t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    valid_urls.place(x=295, y=500)
    
    global invalid_urls
    invalid_urls = Label(rightframe, text= "\n"+str(len(invalid_url)) +"\n\n\tUrls Failed \t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    invalid_urls.place(x = 555, y = 500)
    
    
    
    
    global program_status
    program_status = Label(rightframe, text= "\tStatus: Running \t\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    program_status.place(x = 25, y = 10)
    
    
    
    
    save_step_button = Button(rightframe, text="Download CSV", width = 15,command = lambda:save_validated_data() )
    save_step_button.place(x = 600, y = 10)
    
    

    global validation_thread
    sorting_thread = threading.Thread(target=start_pre_sorting_process, args=(host_name_list,store_name_list), daemon=True) 
    sorting_thread.start()
    
    
    




def check_endpoint_result(count,store_api,product_range):
    
    try:
        time.sleep(0.8)
        product_json = requests.get(store_api).json()
        if("products" in product_json.keys()):
              total_products = len(product_json['products'])
              if(total_products == 0):
                  return True
              else:
                  return False
        else:
            return "Error"
    except Exception as e:
        print(e)
        
 

def pre_sort_products(count,host_name,store_api,store_url):
   lock.acquire()
   try:
       store_endpoint = []
       page_numbers = [4,6,5,51,101,151,201,501,701,801,901,1001,1301,1601,1901,2101,2501,3001,32001,35001,3801,4001,4301,5001,5501,6001,6501,7001,8001,90001,10001]
       for page in page_numbers:
           store_endpoint = (store_api+str(page))
           if(check_endpoint_result(count,store_endpoint,page) == True):
               pre_sort_data_dict[store_api] = [host_name,str(page)]
             
               store =  store_api[8:]
               sep = '/'
               store = store.split(sep, 1)[0]
               text_area_statement(count,store,str(250*page))
               print(store)
               break
              
   except Exception as e:
       print(e)
       
   lock.release()
   
def start_pre_sorting_process(host_name,store_url):
    
    count = 0
    for host,store in zip(host_name,store_url) :
        print(store)
        if(store.count(".") == 1):
            store_api = create_shopify_api_endpoint_for_store_with_www(store)
        else:
            store_api = create_shopify_api_endpoint_for_store(store)
        
       
       
        process_sorting_thread = threading.Thread(target=pre_sort_products, args=(count,host,store_api,store), daemon=True) 
        process_sorting_thread_list.append(process_sorting_thread)
        process_sorting_thread.start()
        count = count + 1