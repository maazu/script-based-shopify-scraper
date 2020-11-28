import subprocess
import os,sys
import time
import glob
import time
import io
import numpy as np
import pandas as pd
from google.colab import files
from multiprocessing import Process
from itertools import chain
import threading
from products_counter import *

start_time = time.time()
global reformat_threads,finished_thread,ended_threads,lock

reformat_thread = []
finished_thread = []
ended_threads = []
lock = threading.Lock()



def download_library():
 
   shopify_lib_repo = "wget -O - -q https://raw.githubusercontent.com/kishaningithub/shopify-csv-download/master/install.sh | sudo sh -s -- -b /usr/local/bin"
   shopify_command_run = subprocess.run(shopify_lib_repo,shell=True)
   print("The exit code was: %d" % shopify_command_run.returncode)

def read_website_df():  
   
    
    csv_file_name = select_csv()

    products_count_data = (count_products(csv_file_name))
    df = pd.DataFrame(list(products_count_data.items()),columns = ['website','total products']) 
    df.sort_values(by=['total products'], inplace=True, ascending=True)
    print("Total runnable urls in file --->", len(df) )   
    df = df['website']
    print("---Sorting Time : {0:.3g} seconds ---".format (time.time() - start_time))
    return df

def read_website_df_single():  
    csv_file_name = select_csv()
    df = pd.read_csv(csv_file_name).drop_duplicates(keep='first').reset_index()
    df = df['website']
    return df



def create_new_directory(location,folder_name):
  
    path = os.path.join(str(location), str(folder_name )+"-"+ str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print(str(folder_name) + "Download directory created: " + str(download_dir))  
    return path



def check_empty(value):
    
    if(pd.isnull(value) == True):
        return True
    else: 
        return value
  
    
  
def shopify_download_command(website_url):
    
    shopify_command = "shopify-csv-download https://www." + website_url +" > "+ str(website_url)+".csv"
    shopify_command_run = subprocess.run(shopify_command,shell=True)  
    #shopify_command_run.stdout.decode('utf-8')
    print("The command exit code was: %d" % shopify_command_run.returncode)
    return shopify_command_run.returncode


def save_failed_csv(location, failed_urls):
    
    summary_directory = create_new_directory(location,"summary_directory")  
    failded_df = pd.DataFrame(columns = ['Failed_URL'])
    failded_df['Failed_URL'] =  pd.Series(failed_urls)  
    failded_df.to_csv(summary_directory+"/"+"Failed-URL-"+ str(generated_time())+".csv", encoding='utf-8-sig' ,index=False)  
    
    
def finish__reformat_threads():
    
    for thread in reformat_thread:
        thread.join()
        
def close_thread(reformat_thread):
    
    reformat_thread[index].join()
    finished_thread.append(index)  
   
    
def trigger_download(download_dir):
    try:
      
        download_dir = download_dir[:-1] + ".zip" 
        print("\n" +  download_dir + "Attempting to trigger download automaticllay ")
        files.download(download_dir)
        print("\n" + download_dir + "Trigger sucessfull....... ")
    
    except Exception as e:
        
        print(e)
        print("\nDownload trigger failed, please download manually....... ")
      
        
      
def zip_data(scraped_folder):
   
  zip_to_download =   scraped_folder[:-1] + ".zip" 
  download_command = "zip -r " +zip_to_download + " " + scraped_folder  
  download_command_run = subprocess.run(download_command,shell=True)
 
  if (download_command_run.returncode == 0):
     
      print(zip_to_download + " zipped folder sucessfully")
      print("Batch compelete -- batch zipped ready for download")
      trigger_download(zip_to_download)
      return True
 
  else:
      print(zip_to_download + " zipped failure")
      return False

        
def step_one(choice,batch_size):
   
    if( choice == "all"):
    
      df = read_website_df() 
    else:
      df = read_website_df_single()
    
    download_dir = create_new_directory("content/","unprocessed")
    processed_dir = create_new_directory("content/","processed")
    WEBSITE_URLS_DF = df.drop_duplicates( keep='first')
    total_count = len(WEBSITE_URLS_DF)
    website_reading_count = 0
    failed_urls = list()
   
    
    for website_url in WEBSITE_URLS_DF:
        website_url = str(website_url)
       
        print(str(website_reading_count+1)+"/"+str(total_count)+" Reading "+ str(website_url) +"...................")  
        
        website_csv_name = str(website_url +".csv")
        
        if(shopify_download_command(website_url) == 0):
            subprocess.call("mv %s %s" % (website_csv_file_name, download_dir), shell=True)
            print("Download Succesful.................")
            
            downloaded_csv_path= download_dir + website_csv_file_name
           
            while(os.path.exists(downloaded_csv_file) == True):
              print("waiting for to be moved....")
              break
          
            thread_count  = website_reading_count
            reformatting_thread = threading.Thread(target= reformat_csv, args=(website_csv_name,downloaded_csv_path,thread_count,batch_size,processed_dir))
            reformat_thread.append(thread)
            reformatting_thread.start() 

        else:
            failed_urls.append(website_url)
            subprocess.call("rm %s" % (website_csv_file_name), shell=True)
            print("Failed Download.................")
        
       
        website_reading_count = website_reading_count + 1
        
        print("======================================\n")
    
   
    save_failed_csv(download_dir, failed_urls)
    finish__reformat_threads()
    print("\n\nDownoload Finished==============================================\n")
    print("\n\nDonwload Directory ===>"+  str(download_dir)) 
    zip_data()
    return download_dir


   
def read_df_from_csv(csv_file_name):
    
    fields = ['Handle','Title', 'Vendor', 'Type', 'Option1 Name' ,'Option1 Value', 'Variant Price','Image Src']
    df = pd.read_csv(csv_file_name, skipinitialspace=True, usecols=fields, keep_default_na=False, na_values=[''],low_memory=False)
    return df

        
def get_unique_products_list(csv_file_name):
   
   df = read_df_from_csv(csv_file_name)    
   print("Total rows in csv: " + str(len(df.index)))
   unique_products = df['Handle'].unique()
   return unique_products
   
def get_all_product_images(df):
   
    product_image_data = {}
    count = 1
    for index, row in df.iterrows():
        product_handle = row['Handle']
        image_Src  = check_empty(str(row['Image Src']))
        
        if(image_Src == True):
            pass 
        
        else:
            
            if (product_handle in product_image_data): 
                if ( image_Src.startswith('https')): 
                    product_image_data[product_handle].append(image_Src)  
            else:
                product_image_data[product_handle]= ([image_Src])
                
    return product_image_data
    

def get_single_product_imgs(product_handle,product_img_dict):
    
     imgs_list =  product_img_dict.get(product_handle)
     if(len(imgs_list) > 0):
        try:
            imgs_list.remove('') 
             
        except Exception as e:
            pass     
     imgs_list = set(imgs_list)
     imgs_list = (list(imgs_list))
     return imgs_list
    

def filter_data(website_name,csv_file_name):
   
    df = read_df_from_csv(csv_file_name)
    products_imgs_data = get_all_product_images(df)
    product_data = {}
    df_list = list()

    for index, row in df.iterrows():
        product_handle = row['Handle']
        title  = row['Title']
        vendor = row['Vendor']
        product_type   = row['Type']
        option1_name = row['Option1 Name']
        option1_value = row['Option1 Value']
        variant_price  = check_empty(row['Variant Price'])
        product_imgs  = get_single_product_imgs(product_handle,products_imgs_data)
        product_url = "https://www." + str(website_name) + "/products/" + str(product_handle)
        if(product_handle in product_data):
          
           if( (check_empty(title) == True) and (check_empty(vendor) == True) and  (check_empty(product_type) == True) and (check_empty(option1_name) == True) and (check_empty(option1_value) == True) and (check_empty(variant_price) == True)):
               pass
           else:
                imgs = ",".join(product_imgs)
                product_data[product_handle].append([product_url,product_handle,title,vendor,product_type,option1_name,option1_value,variant_price,imgs]) 
        else:
            imgs = ",".join(product_imgs)
            product_data[product_handle] = [[product_url,product_handle,title,vendor,product_type,option1_name,option1_value,variant_price,imgs]]

    print("Product images Combined.....")
    return product_data



def convert_into_dataframe(v):
        
        fields = ['Product Url','Handle','Title', 'Vendor', 'Type', 'Option1 Name' ,'Option1 Value', 'Variant Price','Image Src']
        df = pd.DataFrame(v, columns = fields)
        df = df.join(df['Image Src'].str.split(',', expand=True).add_prefix('Image Src '))
        df = df.drop('Image Src', 1)
        df.rename(columns={'Image Src 0': 'Image Src'}, inplace=True)
        
        return df



def reformat_csv(website_name, csv_file_path, thread_count, batch_size, processed_dir):
   
    lock.acquire()
    if (len(finished_thread)  % batch_size == 0):
        print("Batch compelete -- zipping batch for download")
        zip_data(processed_dir)
       
        
        
        
    print("\n\n" + website_name + " Filter begin...\n")
     
    product_data = filter_data(website_name,csv_file_path)
    unique_products = get_unique_products_list(csv_file_path)
    print("\n\n" + website_name + " Total Products: " + str(len(unique_products)))
    
    df_list = list()
   
    for i in unique_products:
        v = np.array(product_data[i])
        
        df_list.append(convert_into_dataframe(v))
    df = pd.concat(df_list)
    
    print("\n\n"+website_name + " dataframe combined.......\nImage reformatted")
    print("\n\n" + website_name + " Total rows after formatting: " + str(len(df.index)))
   
    df.to_csv(processed_dir+website_name+".csv" ,index=False ,encoding="utf-8-sig")
    print("\n\n" + website_name +" Reformat Finished....................\n")
    lock.release()
    close_thread(thread_count)
    
    
    
    
def steps(choice):
  
  download_library()
  download_dir = step_one(choice)
  print("---Sort + Download + Filter Time: {0:.3g} seconds ---".format (time.time() - start_time))
  print("-----------------------Script Finished ------------------------")  
  
  

  
  
if __name__ == "__main__": 
 
  batch_size = input("Enter batch size ============>") 
  choice = input("Filter type \nEnter 'a' for  sort+download+reformat \nEnter 'b' for download+reformat only: \n ====>") 
  if(choice == 'a'):
    steps("all",batch_size)
  elif(choice == 'b'):
    steps("b",batch_size)
  else:
    print("invalid choice")

