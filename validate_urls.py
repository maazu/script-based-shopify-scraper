!pip install aiohttp
# modified fetch function with semaphore
import random
import asyncio
from aiohttp import ClientSession
import pandas as pd
import time
import pprint
import json 
import os
import glob

start_time = time.time()
response_dict = {}
error_dict = {}


def select_csv():
     confirm_dataset = input("Enter 'y' to confirm dataset upload: ")
     if (confirm_dataset == "y"):
        try:
          directory  = os.getcwd() + "/"
          uploaded_csv = glob.glob(directory + "*.csv")
          if (len(uploaded_csv) > 0):
            count = 0
            print("Uploaded files \n")
            print("index \t\tFound_csv_files\n")
            for fcsv in uploaded_csv:
              print(str(count) +"\t\t"+ fcsv)
              count = count + 1
            print("\nCheck the uploaded file in the left bar to make sure it's uploaded .......")
            index_selected = input("Enter the index of the uploaded file: ==>  ")
            index_selected = int(index_selected)
            return uploaded_csv[index_selected]
        except Exception as e:
          print(e)
     else:
        print("please upload the csv dataset")

def create_shopify_api_endpoint_for_store(url):
    url = "https://" + url + "/products.json?limit=250&page=1"  
    return url


def read_website_df_single():  
    csv_file_name = select_csv()
    df = pd.read_csv(csv_file_name).drop_duplicates(keep='first').reset_index()
    return df


def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time



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
    if(type_of_file == "error"):
         df.rename(columns={'Response 0':  'store'}, inplace=True)
    df.rename(columns={'Response 0':  'endpoint'}, inplace=True)
    df.rename(columns={'Response 1': 'status'}, inplace=True)
    df.rename(columns={'Response 2': 'type'}, inplace=True)
    df.to_csv(file_name,index =False, encoding ="utf-8-sig")



async def update_dictionary(hostname,response_url,status,contentType,delay,date): 
    if(contentType == "application/json" or contentType ==  "application/json; charset=utf-8"):
        response_dict[hostname] = [str(response_url), str(status),str(contentType)]
    else:
        error_dict[hostname] = [str(response_url), str(status),str(contentType)]

    print("{} {}:{} with delay {} {}".format(status, contentType, date, response_url, delay,status))  




async def fetch(url, session):
    try:
        hostname = url[8:-31]
        async with session.get(url) as response:
           delay = response.headers.get("DELAY")
           date = response.headers.get("DATE")
           status = response.status
           contentType = response.headers.get('content-type')
           await update_dictionary(hostname,response.url,status,contentType,delay,date)
           return await response.read()
    except Exception as e:
        error_dict[hostname]  = [str(url),"NOT FOUND","NOT FOUND"]
        status = "000"
        print("{} NOT FOUND {}".format(status, url))
        return status
      

async def bound_fetch(sem, url, session):
    
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(store_list): 
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for url in store_list:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
    return task
   



      
if __name__ == "__main__": 
    choice = input("File type:\nEnter 'e' to verify csv\nEnter 'a' for normal run  ===> ")
    df =  read_website_df_single()
    if(choice == "e"):
         store_list = list(df['store'])
    else:                       
        store_list = list(df['store'].apply(create_shopify_api_endpoint_for_store))
    
    print("Total Urls =========> " +str( len(store_list)))
    
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(store_list))
    loop.run_until_complete(future)
    
    print("---Request Compelete total time ==> : {0:.3g} seconds ---".format (time.time() - start_time))
    print("---Creating Validation Summary ---")
   
    summary_dir  = create_new_directory("","validation-summary-"+generated_time())
    add_summary_to_df(response_dict,summary_dir+"/valid-endpoints.csv","valid")    
    add_summary_to_df(error_dict,summary_dir+ "/error-urls.csv","error")
    
    print("--- Validation Summary Folder Created  ---")
    print("---Script total time ==> : {0:.3g} seconds ---".format (time.time() - start_time))
