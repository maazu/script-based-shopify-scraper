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
from pathlib import Path
from json_to_df import *

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


sucess_full_downloads = {}
error_downloads_dict = {}

downloading_process_thread_list = []



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
    geneerated_time = time.strftime("%d-%m-%Y-%H-%M-%S")
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




def downlad_data_from_gui_update(self,dowload_file_path,loaded_dataset_path,main_urls, store_urls):
    
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
    counted_urls_label = Label(rightframe, text= "\n"+str(len(sucess_full_downloads)) +"\n\n\t Urls Counted\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    counted_urls_label.place(x=295, y=500)
    
    global error_urls_label
    error_urls_label = Label(rightframe, text= "\n"+str(len(error_downloads_dict)) +"\n\n\t Urls Failed\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    error_urls_label.place(x = 555, y = 500)
    
    
    
    
    global program_status
    program_status = Label(rightframe, text= "Status: Running\t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    program_status.place(x = 25, y = 10)
    
    
    
    global program_reading_status
    program_reading_status = Label(rightframe, text= "Reading: None\n" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
    program_reading_status.place(x = 25, y = 595)
    
    gui_text_area.insert(END,"{}\t\t{}\t\t{}\t\t\t{}\t".format("0","Status","Products","Store") +'\n')
    gui_text_area.update()
    
  
    global validation_thread
    downloading_thread = threading.Thread(target=start_download_process, args=(host_name_list,store_name_list,dowload_file_path), daemon=True) 
    downloading_thread.start()
    
  
def text_area_statement(count,status,store,product_range):
    try:
        gui_text_area.insert(END,"{}\t\t{}\t\t{}\t\t{}\t".format(count,status,product_range,store) +'\n')
        gui_text_area.update()
        counted_urls_label['text'] = "\n"+str(len(sucess_full_downloads)) +"\n\n\tCounted Urls \t" 
        error_urls_label['text'] = "\n"+str(len(error_downloads_dict)) +"\n\n\tFailed Urls \t"    
        total_urls = str(len(sucess_full_downloads) + len(error_downloads_dict))
        if(total_urls == detected_total_urls):
                Stop()
                program_status['text'] = "\tStatus: Finished \t\t"
                #process_sorting_thread.exit()
               
                  
                    
    except Exception as e:
        
        error_downloads_dict[store] = ["N/A","text area error",str(e)] 
        pass    
    



def check_if_csv_already_exist(host_name_csv):
    
    if(os.path.exists(host_name_csv) == True):  
        return True
    else:
        return False
    
    

  
def start_downloading_data(count,host_name,store_api,store,dowload_file_path):
    lock.acquire()
    try:
        
        df_list = list()
        nextpage = True
        page_number = 0
        store_product_count = [0]
        while (nextpage):
              try:
               
                time.sleep(0.8)
                page_number = page_number + 1
                program_reading_status['text'] = "Reading:Host: "+host_name  +"\nStore: "+ store  +" Page: " +str(page_number)
                
                product_json = requests.get(store_api+str(page_number),allow_redirects=False, timeout=15).json()
                if("products" in product_json.keys()):
                    
                    total_products = len(product_json['products'])
                
                    if((total_products) == 0):
                       nextpage = False
                       store_product_count.append(0)
                       break
                    
                    elif((total_products) > 0):
                            df =  get_products_dataframe(store,product_json)
                            df_list.append(df)
                            store_product_count.append(total_products)
                            
                    
                    elif(total_products > 0 and total_products < 250):
                        if("products" in product_json.keys()):
                            df = get_products_dataframe(store,product_json)
                            df_list.append(df)
                            store_product_count.append(total_products)
                            nextpage = False
                            break
                    else:
                        store_product_count.append(0)
                        nextpage = False
                        break
                    
                
              except Exception as e:
                  store_product_count.append(total_products)
                  error_downloads_dict[store] = [host_name,"Download ERROR",str(e)] 
                  text_area_statement(count+1,"Failed",store,store_product_count)
                  pass
              
      
        store_product_count = str(sum(i for i in store_product_count))
        host_name_csv = str(dowload_file_path +"/"+ host_name+".csv")
        new_df = pd.concat(df_list)
        if(len(df_list) > 0):
            if(check_if_csv_already_exist(host_name_csv) == True):
                 merging_df = []
                 previous_csv_df = pd.read_csv(host_name_csv,index_col = False,low_memory=False)
                 merging_df.append(previous_csv_df)
                 merging_df.append(new_df)
                 final_merged_new_df = pd.concat(merging_df)
                 final_merged_new_df.to_csv(dowload_file_path+ "/"+ host_name+".csv" ,index=False, line_terminator='\n', encoding ="utf-8-sig")
                 sucess_full_downloads [store] = host_name
                 text_area_statement(count+1,"Updated",store,store_product_count)
 
            else:
                new_df.to_csv(dowload_file_path+ "/"+ host_name+".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
                sucess_full_downloads [store] = host_name
                text_area_statement(count+1,"Finished",store,store_product_count)
    
    
    except Exception as e:
        error_downloads_dict[store] = [host_name,"Download ERROR",str(e)] 
      
        pass
    
    if(len(error_downloads_dict) > 0):
        if(check_if_csv_already_exist(dowload_file_path +"/"+ "error-downloads-urls" +".csv") == True):
            os.remove(dowload_file_path +"/"+ "error-downloads-urls" +".csv")
        error_df = pd.DataFrame(list(error_downloads_dict.items()),columns = ['store','hostanderrorcode']) 
        error_df['hostanderrorcode'] = error_df['hostanderrorcode'].apply(list_to_string)
        error_df = error_df.join(error_df['hostanderrorcode'].str.split(',', expand=True).add_prefix('Response '))
        error_df = error_df.drop('hostanderrorcode', 1)
        error_df.rename(columns={'Response 0':  'hostname'}, inplace=True)
        error_df.rename(columns={'Response 1':  'error code'}, inplace=True)
        error_df.to_csv(dowload_file_path +"/"+ "error-downloads-urls" +".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
    
    lock.release()        
               
  
    
  
    
  
def start_download_process(host_name,store_url,dowload_file_path):
    download_directory_name = "stores-data-"+ generated_time()
    import pathlib
    pathlib.Path(dowload_file_path +"/" +download_directory_name ).mkdir(parents=True, exist_ok=True) 
    dowload_file_path = str(dowload_file_path +"/" + download_directory_name)
    
    count = 0
    for host_name,store in zip(host_name,store_url) :
        if(store.count(".") == 1):
            store_api = create_shopify_api_endpoint_for_store_with_www(store)
        else:
            store_api = create_shopify_api_endpoint_for_store(store)
        
       
        global downloading_process_thread
        downloading_process_thread = threading.Thread(target= start_downloading_data, args=(count,host_name,store_api,store,dowload_file_path), daemon=True) 
        downloading_process_thread_list.append(downloading_process_thread)
        downloading_process_thread.start()
        count = count + 1