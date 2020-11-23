#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:45:12 2020

@author: work
"""

import subprocess
import datetime
from functions import *
from converter import *



def create_summary_directory(download_dir):
 
    file_path = download_dir 
    path = os.path.join(download_dir, "Scrapped_summary") 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Summary directory created: " + str(download_dir))  
    return path


def create_reformatted_directory(download_dir):
 
    file_path = download_dir 
    path = os.path.join(download_dir, "Reformatted") 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Reformatted directory created: " + str(download_dir))  
    return path



def step_one():
    
    download_dir =  detect_download_dir()
  
    failed_urls = list()
    failded_df = pd.DataFrame(columns = ['Failed_URL'])
    WEBSITE_URLS_DF = read_website_df().drop_duplicates( keep='first')
    total_count = len(WEBSITE_URLS_DF)
    website_reading_count = 1
    
    
    for website_url in WEBSITE_URLS_DF:
        
        print(str(website_reading_count)+"/"+str(total_count)+" Reading "+ str(website_url) +"...................")  
        
        website_csv_file_name = str(website_url +".csv")
        shopify_command = "shopify-csv-download https://www." + str(website_url)+" > "+ str(website_csv_file_name)
        shopify_command_run = subprocess.run(shopify_command,shell=True)
        print("The exit code was: %d" % shopify_command_run.returncode)
       
        if(shopify_command_run.returncode == 0):
            subprocess.call("mv %s %s" % (website_csv_file_name, download_dir), shell=True)
            print("Download Succesful.................")
        
        else:
            failed_urls.append(website_url)
            subprocess.call("rm %s" % (website_csv_file_name), shell=True)
            print("Failed Download.................")
            
        time.sleep(1)
        website_reading_count = website_reading_count + 1
        print("======================================\n")
        
        
    summary_directory = create_summary_directory(download_dir)    
    failded_df['Failed_URL'] =  pd.Series(failed_urls)  
    failded_df.to_csv(summary_directory+"/"+"Failed-URL-"+ str(generated_time())+".csv", encoding='utf-8-sig' ,index=False)    
    
    print("Downoload Finished..................")
    
    return download_dir



def step_two(download_dir,reformat_dir):
    
  
    sort_and_reformat_csv(download_dir,reformat_dir)
    print("All files has been reformatted.............")
    return download_dir





if __name__ == '__main__':
    
    choice = input("Enter 'DF' to download+filter \nEnter 'D' Just for Downloading\nEnter 'F' for filter already downloaded data\nClick and enter your choice: ==> ")
    if(choice == "DF"):
        
        print_elapsed_time()
        print("Selected choice: Downlaod+Filer ")
        download_dir = step_one()
        print_elapsed_time()
        
        print("==============================================\n")
        print("Moving to Step 2....................")
        
        print_elapsed_time()
        reformat_dir = create_reformatted_directory(download_dir)
        
        sort_and_reformat_csv(download_dir,reformat_dir)
        print_elapsed_time()
     
        
        
    
    elif(choice == "D"):
        
        print("Choice: Downlaod Data Only")
        download_dir = step_one()
   
    elif(choice == "F"):
        print("Choice: Filter Already Downloaded Data Only")
        print("Not supported yet.....")
        print_elapsed_time()
        #download_dir = step_one()   
        
    else:
        print("Invalid Secltion choice")
    
