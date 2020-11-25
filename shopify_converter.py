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
start_time = time.time()
lock = threading.Lock()

def generated_time():
    
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


def download_library():
 
   shopify_lib_repo = "wget -O - -q https://raw.githubusercontent.com/kishaningithub/shopify-csv-download/master/install.sh | sudo sh -s -- -b /usr/local/bin"
  shopify_command_run = subprocess.run(shopify_lib_repo,shell=True)
  print("The exit code was: %d" % shopify_command_run.returncode)

def read_website_df(csv_file_name):  
   
    cwd = os.getcwd()
    file_name = cwd + "/" + str(csv_file_name)
    df = pd.read_csv(str(csv_file_name))
    website_url_df =  df[df.columns[0]].dropna()
    website_Len = len(website_url_df.drop_duplicates())
    print("Total Url Found in file --->", website_Len )   
    return website_url_df


def make_new_directory_mac():
    
    cwd = os.getcwd()
    print(cwd)
    file_path = cwd 
    path = os.path.join(file_path, "shopfiy-scraped-data-"+ str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Download directory created: " + str(download_dir))  
    return path


def create_summary_directory(download_dir):
 
    file_path = download_dir 
    path = os.path.join(download_dir, "Scrapped_summary") 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Summary directory created: " + str(download_dir))  
    return path


def check_empty(value):
    
    if(pd.isnull(value) == True):
        n = ""
        return n
    else: 
        return value
  

def step_one():
   
    
    csv_file_name = input("\nCheck the uploaded file in the left bar to make sure it's uploaded ......."+
    "\nEnter name of the csv file (please make sure the name must match with the file you uploaded\n\n====>")
    download_dir = make_new_directory_mac()

    WEBSITE_URLS_DF = read_website_df(str(csv_file_name)).drop_duplicates( keep='first')
    total_count = len(WEBSITE_URLS_DF)
    website_reading_count = 1
    failed_urls = list()
    failded_df = pd.DataFrame(columns = ['Failed_URL'])
    threads = []
    
    for website_url in WEBSITE_URLS_DF:
        
        print(str(website_reading_count)+"/"+str(total_count)+" Reading "+ str(website_url) +"...................")  
        
        website_csv_file_name = str(website_url +".csv")
        shopify_command = "shopify-csv-download https://www." + str(website_url)+" > "+ str(website_csv_file_name)
        shopify_command_run = subprocess.run(shopify_command,shell=True)
        #shopify_command_run.stdout.decode('utf-8')
        print("The exit code was: %d" % shopify_command_run.returncode)
       
        if(shopify_command_run.returncode == 0):
            subprocess.call("mv %s %s" % (website_csv_file_name, download_dir), shell=True)
            print("Download Succesful.................")
            time.sleep(2)

            downloaded_csv_file = download_dir+website_csv_file_name
            while(os.path.exists(downloaded_csv_file) == True):
              print("waiting for to be moved....")
              break
            thread = threading.Thread(target= reformat_csv, args=(website_csv_file_name,downloaded_csv_file))
            threads.append(thread)
            thread.start() 

        else:
            failed_urls.append(website_url)
            subprocess.call("rm %s" % (website_csv_file_name), shell=True)
            print("Failed Download.................")
            
        website_reading_count = website_reading_count + 1
        print("======================================\n")
    
    
    summary_directory = create_summary_directory(download_dir)    
    failded_df['Failed_URL'] =  pd.Series(failed_urls)  
    failded_df.to_csv(summary_directory+"/"+"Failed-URL-"+ str(generated_time())+".csv", encoding='utf-8-sig' ,index=False)    
    
    for thread in threads:
      
      thread.join()


    print("Downoload Finished..................") 
    return download_dir


   
def read_df_from_csv(csv_file_name):
    
    fields = ['Handle','Title', 'Vendor', 'Type', 'Option1 Name' ,'Option1 Value', 'Variant Price','Image Src']
    df = pd.read_csv(csv_file_name, skipinitialspace=True, usecols=fields, keep_default_na=False, na_values=[''],low_memory=False)
    df.applymap(check_empty)
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
        title  = check_empty(row['Title'])
        vendor = check_empty(row['Vendor'])
        product_type   = check_empty(row['Type'])
        option1_name = check_empty(row['Option1 Name'])
        option1_value = check_empty(row['Option1 Value'])
        variant_price  = check_empty(row['Variant Price'])
        product_imgs  = get_single_product_imgs(product_handle,products_imgs_data)
        product_url = "https://www." + str(website_name) + "/products/" + str(product_handle)
        if(product_handle in product_data):
          
           if((title) =="" and vendor =="" and  product_type == "" and option1_name == "" and option1_value == "" and variant_price == ""):
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



def reformat_csv(website_name,csv_file_name):
   
    lock.acquire()
    print(website_name + " Filter begin...")
     
    product_data = filter_data(website_name,csv_file_name)
    unique_products = get_unique_products_list(csv_file_name)
    print(website_name + " Total Products: " + str(len(unique_products)))
    df_list = list()
    for i in unique_products:
        v = np.array(product_data[i])
        
        df_list.append(convert_into_dataframe(v))
    df = pd.concat(df_list)
    
    print(website_name + " dataframe combined.......\nImage reformatted")
    
    df.to_csv(csv_file_name ,index=False ,encoding="utf-8-sig")
    #df.to_json(csv_file_name[:-4]+".json", orient = 'split', compression = 'infer') 
    print(website_name+ " Total rows after formatting: " + str(len(df.index)))
    print(website_name +" Reformat Finished....................")
    lock.release()



def zip_and_download(scraped_folder,batch_count):
  cwd = os.getcwd()
  scraped_folder_name = os.path.basename(scraped_folder)
  download_file_name = cwd + "Batch-"+str(batch_count)+"-"+scraped_folder_name+".zip"
  download_command = "zip -r " + download_file_name + " " + scraped_folder  
  download_command_run = subprocess.run(download_command,shell=True)
  #download_command_run.stdout.decode('utf-8')
  from google.colab import files
  files.download(download_file_name)


def main():
  download_library()
 
  download_dir = step_one()
  zip_and_download(download_dir,"Full")
  print("Script Finished ..................")
  print("--- Download and Filter Time: {0:.3g} seconds ---".format (time.time() - start_time))
    
    
if __name__ == "__main__":  
    main()
