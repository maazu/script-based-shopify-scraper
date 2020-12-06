import asyncio
from aiohttp import ClientSession
import pandas as pd
import time
import json
import os
import glob

start_time = time.time()
sucess_dict = {}
error_dict = {}
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


def select_csv():
     confirm_dataset = input("Enter 'y' to confirm dataset upload: ")
     if (confirm_dataset == "y"):
        try:
          directory  = os.getcwd() + "/csv-script/"
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



async def update_dictionary(hostname,store_url,response_url,status,contentType,delay,date):

    if(contentType == "application/json" or contentType ==  "application/json; charset=utf-8"):
        sucess_dict[hostname] = [str(store_url),str(response_url), str(status),str(contentType)]
        print(c[0]+ "{} {}:{} with delay {} {}".format(status, contentType, date, response_url, delay,status))
    else:
        error_dict[hostname] = [str(store_url), str(response_url), str(status),str(contentType)]
        print(c[1]+ "{} {}:{} with delay {} {}".format(status, contentType, date, response_url, delay,status))


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

                await update_dictionary(hostname,store_url,response.url,status,contentType,delay,date)

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
        return e


async def bound_fetch(sem, hostname,store, session):

    async with sem:
        await fetch(hostname,store, session)


async def run(host_name_list,store_list):
    tasks = []

    sem = asyncio.Semaphore(1000)
    async with ClientSession() as session:
      for (hostname,store) in zip(host_name_list,store_list):
        try:
          task = asyncio.ensure_future(bound_fetch(sem, hostname,store, session))
          await asyncio.sleep(1)
          tasks.append(task)
        except Exception as e:
          print(e)
      responses = asyncio.gather(*tasks)
      await responses
    return task



def main(host_name_list,store_list):

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(host_name_list,store_list))
    loop.run_until_complete(future)



if __name__ == "__main__":
    download_directory  = os.getcwd() + "/generated-files/"
    summary_dir  = create_new_directory(download_directory,"validation-summary-"+generated_time())

    choice = input("File type:\nEnter 'e' to verify the error csv file \nEnter 'a' for normal run  ===> ")

    df =  read_website_df_single()

    if(choice == "e"):
         host_name_list = list(df['hostname'])
         store_list = list(df['store'])
    else:
        host_name_list = list(df['hostname'])
        store_list = list(df['store'].apply(create_shopify_api_endpoint_for_store))

    print("Total Urls =========> " +str( len(set(host_name_list ))))


    main(host_name_list,store_list)


    print("---Creating Validation Summary ---")
    add_summary_to_df(sucess_dict,summary_dir+"/valid-endpoints.csv","valid")
    add_summary_to_df(error_dict,summary_dir+ "/error-urls.csv","error")
    print("--- Validation Summary Folder created  ---")
    print("---Script total time ==> : {0:.3g} seconds ---".format (time.time() - start_time))
