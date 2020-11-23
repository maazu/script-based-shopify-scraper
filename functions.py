#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 12:32:40 2020

@author: Acer
"""
import os,sys
from pathlib import Path
cwd = str(Path(__file__).parent)
sys.path.insert(0, cwd)
import time
import glob
import time
import numpy as np
import pandas as pd
from tkinter import *
from sys import platform
from tkinter import filedialog


def intro():
    print("\n********************Shopify Script Based Scrapper **********************")    
    print("*****************************************************************************")
    print("***************************************************************************\n")

 

def ask_file_directory():
    root = Tk()
    root.withdraw()
    root.update()
    dataSet_file_directory = filedialog.askopenfilename()
    #dataSet_file_directory = str(os.getcwd()) + "/files/dataset/website_urls.csv"
    #print(dataSet_file_directory)
    return dataSet_file_directory


           
def check_file_format(provided_file):
    file_name = os.path.basename(provided_file)
    if(file_name.endswith(".csv")):
        return 1
    else:
        return 0  



def read_dataframe(data_file):
    if(check_file_format(data_file) == 1):
        df = pd.read_csv(data_file)
        df =  df[df.columns[0]].dropna()
        return df 
    elif(check_file_format(data_file) == 2):
        df = pd.read_excel(open(data_file,'rb'), sheet_name='Sheet 1')
    return df


def read_website_df():
    website_url_dataset_path = ask_file_directory()
    website_url_df = read_dataframe(website_url_dataset_path)
    website_Len = len(read_dataframe(website_url_dataset_path).drop_duplicates())
   
    print("Selected Data File Consist Of Website Url --->", os.path.basename(website_url_dataset_path))
    print("Total Url Found in file --->", website_Len )
    return website_url_df

   

    
def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time



def make_new_directory_mac():
    cwd = os.getcwd()
    print(cwd)
    file_path = cwd +"/files/scraped-data/"
    path = os.path.join(file_path, "shopfiy-scraped-data-"+str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Download directory created: " + str(download_dir))  
    return path



def make_new_directory_mac():
    cwd = os.getcwd()
    print(cwd)
    file_path = cwd +"/files/scraped-data/"
    path = os.path.join(file_path, "shopfiy-scraped-data-"+str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Download directory created: " + str(download_dir))  
    return path







def make_new_directory_windows():
    cwd = os.getcwd()
    print(cwd)
    file_path = cwd +"\\files\\scraped-data\\"
    path = os.path.join(file_path, "shopfiy-scraped-data-"+str(generated_time()+"\\")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print("Download Directory created: " + str(download_dir))  
    return path


def detect_download_dir():
    
    if platform == "darwin" or platform == 'linux':
        
        download_dir = make_new_directory_mac()
        return download_dir
    
    if platform == "win32":
        
        download_dir = make_new_directory_windows()
        return download_dir
    
    else:
        print("Operating system not supported..")
        print(platform)





def get_chrome_driver(download_dir):
    
    if platform == "darwin":
        try:
          
            preferences = {"download.default_directory": download_dir ,
                       "download.prompt_for_download": False}
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", preferences)
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            # options.add_argument("--user-data-dir='~/Library/Application Support/Google/Chrome'")
            #options.add_argument('--profile-directory=Default')
            options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            chrome_driver_binary = "/usr/local/bin/chromedriver"
            options.add_extension('1.9.10.26_0.crx')
            driver = webdriver.Chrome(chrome_driver_binary, options=options)
            #print(driver.desired_capabilities)
            return driver
        
        except Exception as e:
            
            print(e)
            print("Driver Import Error")
            raise(e)
    
    if platform == "win32":
        try:
            
            preferences = {"download.default_directory": download_dir ,
                       "download.prompt_for_download": False}
            options = webdriver.ChromeOptions()
            #options.add_argument('headless')
            options.add_experimental_option("prefs", preferences)
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            options.add_extension('1.9.10.26_0.crx')
            driver_path = "chromedriver/windows/chromedriver.exe"
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
            #print (driver.desired_capabilities)
            return driver
        
        except Exception as e:
            
            print(e)
            print("Driver Import Error")
            
            



  


    


  
def check_delay(browser_closing_delay):
    if(browser_closing_delay == ''):
        browser_closing_delay = 30
        return browser_closing_delay
    else:
        browser_closing_delay = int(browser_closing_delay)
        return browser_closing_delay

        

        





def make_attempts(website,download_dir,delay_time,limit):
    
     attempt = 1  
     status = rename_downloaded_csv(website,download_dir)       
     while(status != True):               
          additional_time = 60
          delay_time = delay_time + additional_time
          print("Attempting to download again after increasing time delay.... Attempt Count "+ str(attempt) )
          extract_using_extension(website,download_dir,delay_time)
          status = rename_downloaded_csv(website,download_dir)
          attempt = attempt + 1
          if(attempt == limit):
              
              break
     print(website + " Product csv file donwonload Status: "+  str(status))
     
            
            
   