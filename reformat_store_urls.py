# -*- coding: utf-8 -*-
#!/usr/bin/env python3


"""
Created on Wed Dec  2 16:34:36 2020

@author: Maaz
"""
import pandas as pd
import time
import os
import glob
import numpy as np

start_time = time.time()


def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time



def create_new_directory(location,folder_name):
  
    path = os.path.join(str(location), str(folder_name )+"-"+ str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print(str(folder_name) + " directory created: " + str(download_dir))  
    return path


def read_website_df_single(data_set_path): 
    try:
        df = pd.read_csv(data_set_path,index_col = False ).drop_duplicates(keep='first')
        return df
    except Exception as e:
        print("Csv file is not found in the file or data is not uploaded")
             
             
def remove_asterik(s):  
    str1 = s.replace("*","")
    str1 = str1.replace("/","")
    return str1


def add_summary_to_df(sum_dictionary,file_name,type_of_file):

    download_directory  = os.getcwd() + "/generated-files/"
    df = pd.DataFrame(list(sum_dictionary.items()),columns = ['hostname','store'])  
    
    df = df.join(df['store'].str.split(';', expand=True).add_prefix('store'))
    df = df.drop('store', 1) 
    df = df.set_index(['hostname']).stack().reset_index(name='store')
    df = df.drop('level_1', 1)
    
    df['store'] = df['store'].apply(remove_asterik)
    
    return df
    



def start_reformating_script(data_set_path,main_urls,store_urls,rightframe,):
    df = read_website_df_single(data_set_path)
   
    url_dictionary = {}
    for index, row in df.iterrows():
        url_dictionary[row[main_urls]] = row[store_urls]
    df = add_summary_to_df(url_dictionary,"/store-data-reformated-"+generated_time()+".csv","current_directory")
    return df
    
    
def save_reformatted_df(df,save_data_set_path):
     df.to_csv(save_data_set_path+"/reformatted-csv-"+generated_time()+".csv",index = False, encoding = "utf-8-sig")
     confrimation = "Reformat csv file has been sucessfully"
     return confrimation
     

"""
if __name__ == "__main__": 
   
    
    df = read_website_df_single()
    print("please wait................it can take upto 5 minute for large files")
    url_dictionary = {}
    for index, row in df.iterrows():
        url_dictionary[row['Domain']] = row['Location on Site']
           
    add_summary_to_df(url_dictionary,"/store-data-reformated-"+generated_time()+".csv","current_directory")
    print("CSV File reformatted .....................")
    print("---Total Reforamting Time: {0:.3g} seconds ---".format (time.time() - start_time))
"""