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
from validate_urls import *
from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename
import threading

counter = 66600
running = False
valid_url = {}
invalid_url = {}
gui_text_area_updates = []
active_valid_thread = []

standard_font_name = "Motiva Sans"
rightframe_background_color = "#EDE9D8"
foreground_color = "#173630"
font_weight ="bold"
button_background_color = "#108043"
text_font_size = 12



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
              

def get_store_data(dataset_path,host_col_name,store_col_name):
    
  df = pd.read_csv(dataset_path).drop_duplicates(keep='first').reset_index()
  total_urls = len(list(df[store_col_name]))
  host_name_list = list(df[host_col_name])
  store_list = list(df[store_col_name])
  store_list = list(map(create_shopify_api_endpoint_for_store,store_list))
  return [total_urls,host_name_list,store_list ]   




def validation_process_gui_update(self,loaded_dataset_path,main_urls,store_urls):
    
    
        
    self.root.update()
    global rightframe
    rightframe = Frame(self.root,bg =  rightframe_background_color)  
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    startTime = datetime.now()
    kill_previous_thread()
   
    valid_url.clear()
    invalid_url.clear()
  
    global elapsed_time
    elapsed_time = Label(rightframe, text="", font=(standard_font_name, 20,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")  
    elapsed_time.place(x = 180, y = 650)
    
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
   
    global valid_urls
    valid_urls = Label(rightframe, text= "\n"+str(len(valid_url)) +"\n\n\tUrls Valid \t" ,font=(standard_font_name, text_font_size,font_weight),bg =rightframe_background_color,fg = foreground_color,borderwidth=2, relief="solid")
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
    global stop_validation_thread
    validation_thread = threading.Thread(target=start_validation_process, args=(loaded_dataset_path,main_urls,store_urls,), daemon=True) 
    active_valid_thread.append(validation_thread)
    validation_thread.start()
    
    
    
def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


def create_shopify_api_endpoint_for_store(url):
    url = "https://" + url + "/products.json?limit=250&page=1"  
    return url


def create_shopify_api_endpoint_for_store_with_www(url):
    url = "https://www." + url + "/products.json?limit=250&page=1"  
    return url

def create_shopify_api_endpoint_for_store_with_http(url):
    url = "http://" + url + "/products.json?limit=250&page=1"  
    return url
    


 
                        
def save_df_to_selected_path(user_selected_path):
   
    valid_df = pd.DataFrame(list(valid_url.items()),columns = ['valid store','hostname']) 
    
    valid_df.to_csv(user_selected_path +"/"+ "valid-urls-"+ generated_time() +".csv",index=False, line_terminator='\n', encoding ="utf-8-sig")
    
    invalid_df = pd.DataFrame(list(invalid_url.items()),columns = ['Invalid store','host']).dropna()
    
    invalid_df.to_csv(user_selected_path+"/"+ "invalid-urls-"+ generated_time() +".csv", index=False, line_terminator='\n', encoding ="utf-8-sig")



def save_validated_data():
    save_data_set_path = filedialog.askdirectory (initialdir="/", title="Select a directory", ) # select a video file from the hard drive
    if ( save_data_set_path != ''):
        save_thread = threading.Thread(target=save_df_to_selected_path, args=(save_data_set_path,), daemon=True)  
        save_thread.start()
        confirmation = "Valid and invalid csv file has been saved sucessfully"
        mbox.showinfo("Information", confirmation)
        save_thread.join()
  
async def text_area_statement(validity_status,host,store,count,contentType):
    

    store_url =  store[8:]
    sep = '/'
    store_url = store_url.split(sep, 1)[0]
    total =  str(len(valid_url) + len(invalid_url) )
    gui_text_area_updates.append([validity_status,store_url,total])
    #print("{}\t\t {}\t\t {}\t\t {}\t\t {}\t\t  ".format(validity_status ,str(len(valid_url)),str(len(invalid_url)),total,store_url)) 
    gui_text_area.insert(END,"{}\t\t {}\t\t {}\t\t ".format(total,validity_status,store_url)+'\n')
    gui_text_area.update()
    valid_urls.configure(text="\n"+str(len(valid_url)) +"\n\n\tValid Urls \t")
    invalid_urls.configure(text="\n"+str(len(invalid_url)) +"\n\n\tFailed Urls \t")
    
    if (detected_total_urls == total ):
        program_status.configure(text="\tStatus: Finished \t\t") 
        Stop()
        
       
 
    await asyncio.sleep(0.5)



async def update_url_validity_status(validity_status,host,store,count,contentType):
    store_url =  store[8:]
    sep = '/'
    store_url = store_url.split(sep, 1)[0]
    if(validity_status == "valid"):
        
        valid_url[store_url] = host
    else:
       
        invalid_url[store_url] = host
    
    await text_area_statement(validity_status,host,store,count,contentType)
   
             

async def fetch(host: str,store: str,count: int, session: ClientSession, **kwargs) -> tuple:
    try:
        
        store_url = store[8:-31]
        
        if(store_url.count(".") == 1):
            store = create_shopify_api_endpoint_for_store_with_www(store_url)
            
        async with session.get(store) as response:
            await asyncio.sleep(0.50)
            await response.read()
            
            status = response.status
            contentType = response.headers.get('content-type')
            
            if (status == 200 and contentType == "application/json" or status == 200 and contentType == "application/json; charset=utf-8"):
                json_data = await response.json()
             
                if('products' in json_data.keys()):
                    
                    await update_url_validity_status("valid",host,str(response.url),count,contentType)   
                    
                else:
                    
                     await update_url_validity_status("invalid",host,str(response.url),count,contentType)   
                     
            else:
               
                 await update_url_validity_status("invalid",host,str(response.url),count,contentType)   
                
            
    except Exception as e:
        #print(e)
        validity_status = "invalid"
        contentType = "unknown"
        await update_url_validity_status(validity_status,host,store,count,contentType)
        await asyncio.sleep(0.50)
        pass
             
                

async def bound_fetch(sem, hostname,store,count, session):

    async with sem:
        await fetch(hostname,store, count, session)
        
        
        

async def run(host_name_list,store_list): 
    tasks = []
    sem = asyncio.Semaphore(1000)
    async with ClientSession() as session:
      count = 0
      for (hostname,store) in zip(host_name_list,store_list):
        
        try:
           
            task = asyncio.ensure_future(bound_fetch(sem, hostname,store,count,session))
            await asyncio.sleep(1)
            tasks.append(task)
            count = count + 1
            
        except Exception as e:
            #print(e)
            pass
          
      #print("URLS TASK CREATED")
      responses = asyncio.gather(*tasks)
      await responses

    return task




def start_validation_process(dataset_path,host_col_name,store_col_name):
    from functools import wraps

    from asyncio.proactor_events import _ProactorBasePipeTransport
    
    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise
        return wrapper
    
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
  
    asyncio.run(run(host_name_list,store_name_list))
  
  


if __name__ == "__main__":
    
  
   print("--- Total Validation Time: --- >>" + str(datetime.now() - startTime))