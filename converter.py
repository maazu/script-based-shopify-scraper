# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on Thu Nov 12 19:09:58 2020

@author: Maaz
"""

import pandas as pd
import numpy as np
import pandasql as ps
from itertools import chain
import glob
import os

def check_empty(value):
    if(str(value) == "nan"):
        n = ""
        return n
    else: 
        return value
  
    
  
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
        image_Src =check_empty( row['Image Src'])
        
        if(product_handle in product_image_data):
           
            if( image_Src.startswith('https')):
                
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
    
    
#tiger-of-sweden-jeans-evole-en-bleu-royal-25d

count = 1  
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
        variant_price  = row['Variant Price']
        product_imgs  = get_single_product_imgs(product_handle,products_imgs_data)
        product_url = "https://www." + str(website_name) + "/products/" + str(product_handle)
        if(product_handle in product_data):
            
            
            imgs = ",".join(product_imgs)
            product_data[product_handle].append([product_url,product_handle,title,vendor,product_type,option1_name,option1_value,variant_price,imgs])
          
            
        else:
            imgs = ",".join(product_imgs)
            product_data[product_handle] = [[product_url,product_handle,title,vendor,product_type,option1_name,option1_value,variant_price,imgs]]
                 
  
    #print((product_data["tiger-of-sweden-jeans-evole-en-bleu-royal-25d"]))
    print("Product images Combined.....")
    return product_data



def convert_into_dataframe(v):
        
        fields = ['Product Url','Handle','Title', 'Vendor', 'Type', 'Option1 Name' ,'Option1 Value', 'Variant Price','Image Src']
        df = pd.DataFrame()
        
        df["Product Url"],df["Handle"], df["Title"],df["Vendor"],df["Type"],df["Option1 Name"],df["Option1 Value"],df["Variant Price"],df["Image Src"] = v.T
        
        return df



def reformat_csv(website_name,csv_file_name):

    print("Filter begin...")
     
    product_data = filter_data(website_name,csv_file_name)
    unique_products = get_unique_products_list(csv_file_name)
    print("Total Products: " + str(len(unique_products)))
    df_list = list()
    
    
    
    for i in unique_products:
        v = np.array(product_data[i])
        
        df_list.append(convert_into_dataframe(v))
    
    
    
    df = pd.concat(df_list)[df_list[0].columns]
    
    print("Almost done............")
    row_list = []
    
    for index, row in df.iterrows():
            product_url = check_empty(row['Product Url'])
            Handle = check_empty(row['Handle'])
            Title  = check_empty(row['Title'])
            Vendor = check_empty(row['Vendor'])
            Type   = check_empty(row['Type'])
            Option1_Name = check_empty(row['Option1 Name'])
            Option1_value = check_empty(row['Option1 Value'])
            Variant_Price  = check_empty(row['Variant Price'])
            Image_Src = check_empty(row['Image Src'])
            
            if(Title =="" and Vendor =="" and  Type == "" and Option1_Name == "" and Option1_value == "" and Variant_Price == ""):
               pass
            else:
                row_list.append([product_url,Handle,Title,Vendor,Type,Option1_Name,Option1_value,Variant_Price,Image_Src])
          
                 
    v2 = np.array(row_list)                
    df22 = convert_into_dataframe(v2)  
    

    df22 = df22.join(df22['Image Src'].str.split(',', expand=True).add_prefix('Image Src '))
    print("dataframe combined.......\nImage reformatted")
    df22 = df22.drop('Image Src', 1)
    df22.rename(columns={'Image Src 0': 'Image Src'}, inplace=True)
    
    df22.to_csv(csv_file_name,index=False ,encoding="utf-8-sig")
    print("Total rows after formatting: " + str(len(df22.index)))
    print("Reformat Finished....................")




for path in glob.glob('dataset/*.csv'): 
  
    website_name  = os.path.basename(path)[:-4]
    csv_file_path = path
    print(website_name + " reformatting")
    reformat_csv(website_name,csv_file_path)
    print(website_name + " reformatting finished\n") 
    
