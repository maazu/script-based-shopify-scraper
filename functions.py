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



def print_elapsed_time(prefix=''):
    e_time = time.time()
    if not hasattr(print_elapsed_time, 's_time'):
        print_elapsed_time.s_time = e_time
    else:
        print(f'{prefix} elapsed time: {e_time - print_elapsed_time.s_time:.2f} sec')
        print_elapsed_time.s_time = e_time
  
    
