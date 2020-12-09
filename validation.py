import asyncio
from aiohttp import ClientSession
import pandas as pd
import time
import json 
import os
import glob
from json_to_df import *

start_time = time.time()
sucess_dict = {}
error_dict = {}
df_list = list()


c = (
    "\033[0m",   # End of 
    color
    
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time



def create_shopify_api_endpoint_for_store(url):
    url = "https://" + url + "/products.json?limit=250&page=1"  
    return url


def read_website_df_single():  
    csv_file_name = select_csv()
    df = pd.read_csv(csv_file_name).drop_duplicates(keep='first').reset_index()
    return df



def create_new_directory(location,folder_name):
  
    path = os.path.join(str(location), str(folder_name )+"-"+ str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print(str(folder_name) + " directory created: " + str(download_dir))  
    return path


def listToString(s):  
    str1 = "," 
    return (str1.join(s)) 


def add_summary_to_df(sum_dictionary,file_name,type_of_file):
  
    df = pd.DataFrame(list(sum_dictionary.items()),columns = ['hostname','server respone']) 
    df['server respone'] = df['server respone'].apply(listToString)
    df = df.join(df['server respone'].str.split(',', expand=True).add_prefix('Response '))
    df = df.drop('server respone', 1)
    
    df.rename(columns={'Response 0':  'store'}, inplace=True)
    df.rename(columns={'Response 0':  'endpoint'}, inplace=True)
    df.rename(columns={'Response 1': 'status'}, inplace=True)
    df.rename(columns={'Response 2': 'type'}, inplace=True)
    df.to_csv(file_name,index =False, encoding ="utf-8-sig")



async def update_dictionary(hostname,store_url,response_url,status,contentType,delay,date,response): 
    
    if(contentType == "application/json" or contentType ==  "application/json; charset=utf-8"):
        json_data = await response.json()
        
        sucess_dict[hostname] = [str(store_url),str(response_url), str(status),str(contentType)]
        print(c[0]+ "{} {}:{} with delay {} {}".format(status, contentType, date, response_url, delay,status)) 
      
        df = await  get_products_dataframe(store_url,json_data)
        df_list.append(df)     
        #print(df)
       
            
        print("Total dataframe ====================>"+ str(len(df_list)))
        await asyncio.sleep(1)
       
        
    else:
        error_dict[hostname] = [str(store_url), str(response_url), str(status),str(contentType)]
        print(c[1]+ "{} {}:{} with delay {} {}".format(status, contentType, date, response_url, delay,status))  
        await asyncio.sleep(1)
             

async def fetch(hostname,store, session):
    try:
        store_url = store[8:-31]
        try:  
            async with session.get(store) as response:
                await asyncio.sleep(1)
                delay = response.headers.get("DELAY")
                date = response.headers.get("DATE")
                status = response.status
                contentType = response.headers.get('content-type')
               
                await update_dictionary(hostname,store_url,response.url,status,contentType,delay,date,response)
                await asyncio.sleep(1)
        except Exception as e:
            error_dict[hostname]  = [store,store_url,"NOT FOUND","NOT FOUND"]
            status = "000"
            print("{} NOT FOUND {}".format(status, store))
            print(e)
            pass 
                       
    except Exception as e:
        error_dict[hostname]  = [store,store_url,"NOT FOUND","NOT FOUND"]
        status = "000"
        print("{} NOT FOUND {}".format(status, store))
        print(e)
        return e
      

async def bound_fetch(sem, hostname,store, session):

    async with sem:
        await fetch(hostname,store, session)


async def run(host_name_list,store_list): 
    tasks = []
  
    sem = asyncio.Semaphore(1000)
    async with ClientSession() as session:
      for (hostname,store) in zip(host_name_list,store_list):
        count = 0
        try:
          for i in range(0,1000):
              
              store = "https://" + store_list[count] + "/products.json?limit=250&page=" +str(i)
              print(store) 
              task = asyncio.ensure_future(bound_fetch(sem, hostname,store, session))
              
              tasks.append(task)
             
              await asyncio.sleep(1)
              
        except Exception as e:
          print(e)
        
      count = count + 1 
   
      
      responses = asyncio.gather(*tasks)
      await responses

    return task
   


def main(host_name_list,store_list):
    
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(host_name_list,store_list)) 
    loop.run_until_complete(future)










   
if __name__ == "__main__": 
   
 
    
    host_name_list = ["jostens.com"]

    store_list = ["schoolstore.jostens.com"]
    
    task = main(host_name_list,store_list)
    
    print("---Total Reforamting Time: {0:.3g} seconds ---".format (time.time() - start_time))
