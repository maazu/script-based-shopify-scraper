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
import tkinter.scrolledtext as tkscrolled


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
error_soriting_data_dict = {}

process_sorting_thread_list = []



def counter_label(label,startTime):  
   
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
    
def Start(label,startTime):  
    global running  
    running=True
    counter_label(label,startTime)  

    
def Stop():  
    global running  
   
    running = False
    

def kill_previous_thread():
    if(len(active_valid_thread) > 0):
        active_valid_thread[0].shutdown = True
       
        active_valid_thread.clear()


    
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
    


def list_to_string(list_column):
     data = ','.join(map(str, list_column)) 
     return data
                        
def save_df_to_selected_path(user_selected_path):

    sorted_df = pd.DataFrame(list(pre_sort_data_dict.items()),columns = ['sorted store','hostandcountlist']) 
    if(len(sorted_df) > 0):
        sorted_df['hostandcountlist'] = sorted_df['hostandcountlist'].apply(list_to_string)
        sorted_df = sorted_df.join(sorted_df['hostandcountlist'].str.split(',', expand=True).add_prefix('Response '))
        sorted_df = sorted_df.drop('hostandcountlist', 1)
        sorted_df.rename(columns={'Response 0':  'hostname'}, inplace=True)
        sorted_df.rename(columns={'Response 1':  'count'}, inplace=True)
        sorted_df['count'] = sorted_df['count'].astype(str).astype(int)
        sort_by_count = sorted_df.sort_values('count')
        sorted_df.sort_values('count')
        sort_by_count.to_csv(user_selected_path +"/"+ "valid-sorted-urls-"+ generated_time() +".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
        sort_by_count.drop(sorted_df.index, inplace=True)
    sorted_df.to_csv(user_selected_path +"/"+ "valid-sorted-urls-"+ generated_time() +".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
    sorted_df.drop(sorted_df.index, inplace=True)
    
    
    error_df = pd.DataFrame(list(error_soriting_data_dict.items()),columns = ['store','hostanderrorcode']) 
    if(len(error_df) < 0):
        error_df['hostanderrorcode'] = sorted_df['hostanderrorcode'].apply(list_to_string)
        error_df = error_df.join(error_df['hostanderrorcode'].str.split(',', expand=True).add_prefix('Response '))
        error_df = error_df.drop('hostanderrorcode', 1)
        error_df.rename(columns={'Response 0':  'hostname'}, inplace=True)
        error_df.rename(columns={'Response 1':  'error code'}, inplace=True)
    
        error_df.to_csv(user_selected_path +"/"+ "error-sorted-urls-"+ generated_time() +".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
    



def save_sorted_data():
    save_data_set_path = filedialog.askdirectory (initialdir="/", title="Select a directory", ) # select a video file from the hard drive
    if ( save_data_set_path != ''):
        save_thread = threading.Thread(target=save_df_to_selected_path, args=(save_data_set_path,), daemon=True)  
        save_thread.start()
        confirmation = "Sorted data csv file has been saved sucessfully"
        mbox.showinfo("Information", confirmation)
        save_thread.join()
    else:
        error = "the directory was not selected "
        mbox.showerror("Error", error)


    
            
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
    startTime = datetime.now()
    #kill_previous_thread()
   
    
    
    global elapsed_time
    elapsed_time = Label(rightframe, text="", font=(standard_font_name, 20,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")  
    elapsed_time.place(x = 180, y = 650)
    startTime = datetime.now()
    Start(elapsed_time,startTime)
  
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
   
    global counted_urls_label
    counted_urls_label = Label(rightframe, text= "\n"+str(len(pre_sort_data_dict)) +"\n\n\t Urls Counted\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    counted_urls_label.place(x=295, y=500)
    
    global error_urls_label
    error_urls_label = Label(rightframe, text= "\n"+str(len(error_soriting_data_dict)) +"\n\n\t Urls Failed\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    error_urls_label.place(x = 555, y = 500)
    
    
    
    
    global program_status
    program_status = Label(rightframe, text= "\tStatus: Running \t\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    program_status.place(x = 25, y = 10)
    
    
    
    
    save_step_button = Button(rightframe, text="Download CSV", width = 15,command = lambda:save_sorted_data() )
    save_step_button.place(x = 600, y = 10)
    
    #global counting_progress_bar
    #counting_progress_bar = Progressbar(rightframe,orient=HORIZONTAL,length=100,mode='determinate')
    #
    global validation_thread
    sorting_thread = threading.Thread(target=start_pre_sorting_process, args=(host_name_list,store_name_list), daemon=True) 
    sorting_thread.start()
    
  
def text_area_statement(count,status,store,product_range):
    try:
        gui_text_area.insert(END,"{}\t\t{}\t\t{}\t\t{}\t".format(count,status,product_range,store) +'\n')
        gui_text_area.update()
        counted_urls_label['text'] = "\n"+str(len(pre_sort_data_dict)) +"\n\n\tCounted Urls \t" 
        error_urls_label['text'] = "\n"+str(len(error_soriting_data_dict)) +"\n\n\tFailed Urls \t"    
        total_urls = str(len(pre_sort_data_dict) + len(error_soriting_data_dict))
        if(total_urls == detected_total_urls):
                Stop()
                program_status['text'] = "\tStatus: Finished \t\t"
                #process_sorting_thread.exit()
            
    except Exception as e:
        
        error_soriting_data_dict["N/A"] = ["N/A","SORTING ERROR",str(e)]
        pass    
    

def check_endpoint_result(count,host_name,store_api,product_range):
    store =  store_api[8:]
    sep = '/'
    store = store.split(sep, 1)[0]
    try:
        time.sleep(0.8)
        product_json = requests.get(store_api).json()
        if("products" in product_json.keys()):
              total_products = len(product_json['products'])
              if(total_products == 0):
                  return "zero products"
              elif(total_products > 0 and total_products < 250):
                  return "zero products"
              else:
                  return "more products"
        
    except Exception as e:
        text_area_statement(count,"Failed",store,"Logged")
        error_soriting_data_dict[store] = [host_name,"SORTING ERROR",str(e)]
        return False
    
    


def pre_sort_products(count,host_name,store_api,store_url):
   lock.acquire()
   store =  store_api[8:]
   sep = '/'
   store = store.split(sep, 1)[0]
   
   
   try:
       store_endpoint = []
       page_numbers = [1,2,4,6,5,10,20,40,50,60,80,101,120,151,201,501,701,801,901,1001,1301,1601,1901,2101,2501,3001,3201,3501,3801,4001,4301,4500,5001,5501,6001,6501,7001,8001,9001,10001]
       text_area_statement(count+1,"Ongoing",store,"Counting")
       for page in page_numbers:
           store_endpoint = (store_api+str(page))
           
           if(check_endpoint_result(count,host_name,store_endpoint,page) == "zero products"):
               pre_sort_data_dict[store_url] = [host_name,str(250*page)]

               text_area_statement(count+1,"Found",store,str(250*page))
              
               break
           
              
   except Exception as e:
       text_area_statement(count,"Failed",store,"Logged")
       error_soriting_data_dict[store_url] = [host_name,"SORTING ERROR",str(e)]
       
   lock.release()
  
   
  
    
  
    
  
def start_pre_sorting_process(host_name,store_url):
    
    count = 0
    for host,store in zip(host_name,store_url) :
        if(store.count(".") == 1):
            store_api = create_shopify_api_endpoint_for_store_with_www(store)
        else:
            store_api = create_shopify_api_endpoint_for_store(store)
        
       
        global process_sorting_thread
        process_sorting_thread = threading.Thread(target=pre_sort_products, args=(count,host,store_api,store), daemon=True) 
        process_sorting_thread_list.append(process_sorting_thread)
        process_sorting_thread.start()
        count = count + 1