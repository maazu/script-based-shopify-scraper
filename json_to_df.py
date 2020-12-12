# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 15:03:36 2020

@author: Maaz
"""
import asyncio
import pandas as pd
import re

def get_option_names(product_count,product_dict,option_positon):
    total_options = len(product_dict['options'])
    option_name = ['','','']
    for option_number in range(0, total_options):
        option_name[option_number] = (product_dict['options'][option_number]["name"])

    if(option_positon == 1):
        return option_name[0]
    elif(option_positon == 2):
        return option_name[1]
    elif (option_positon == 3):
        return option_name[2]
    else:
        #print("invalid request")
        return ""


def get_single_variant_option_value(product_count,variant_number,product_dict,option_name):
    
    option_value = product_dict['variants'][variant_number][option_name]
    
    return option_value

def get_single_variant_price(product_count,variant_number,product_dict,price):
    
    price = product_dict['variants'][variant_number][price]
    
    return price


def get_product_images(product_count,product_dict):
    
    total_images = len(product_dict['images'])
    product_imgs = list()
    for image_number in range(0, total_images):
        product_imgs.append((product_dict['images'][image_number]['src']))
    separator = ','
    product_imgs = (separator.join(product_imgs))
    return product_imgs



def get_products_dataframe(website_name,product_json):
    
    products_records = []
  
    total_products = len(product_json['products'])
    for i in range(0,total_products):
      
        product_count = i
        
        try:
            title = (product_json['products'][product_count]['title'])
            handle = (product_json['products'][product_count]['handle'])
            body_html = (product_json['products'][product_count]['body_html'])
            try:
                body_html = re.sub(r"[\n\t\s]*", "", body_html)
            except:
                pass
               
            vendor = (product_json['products'][product_count]['vendor'])
            product_type = (product_json['products'][product_count]['product_type'])
            product_tag = (product_json['products'][product_count]['tags'])
            try:
                product_tag = ",".join(str(x) for x in product_tag)
            except:
                pass  
            total_variants = (len(product_json['products'][product_count]['variants']))
            product_url = "https://" + str(website_name) + "/products/" + str(handle)
            #print("Total variants ==> " + str(total_variants))
            product_dic = product_json['products'][product_count]
                
            for variant_num in range(0,total_variants):  
                variant_number = variant_num
                
               
                option1_name = get_option_names(product_count,product_dic,1)
                option2_name = get_option_names(product_count,product_dic,2)
                option3_name = get_option_names(product_count,product_dic,3)  
                option1_value = (get_single_variant_option_value(product_count,variant_number,product_dic,"option1"))
                option2_value = (get_single_variant_option_value(product_count,variant_number,product_dic,"option2"))
                option3_value = (get_single_variant_option_value(product_count,variant_number,product_dic,"option3"))
                variant_price  = (get_single_variant_price(product_count,variant_number,product_dic,"price"))
                product_images = get_product_images(product_count,product_dic)
                
                products_records.append([product_url,handle,title,body_html,vendor,product_type,product_tag,option1_name,option1_value,option2_name,option2_value,option3_name,option3_value,variant_price,product_images])
       
        except Exception as e:
            #print("Exception row > " + str(e) )
            #print(e)
            pass
    
    
   
    fields = ['URL','Handle','Title', 'Body (HTML)','Vendor', 'Type','Tags','Option1 Name','Option1 Value','Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value','Variant Price','Image Src']
    df = pd.DataFrame(products_records,columns = fields)
    df = df.join(df['Image Src'].str.split(',', expand=True).add_prefix('Image Src '))
    df = df.drop('Image Src', 1)
    df.rename(columns={'Image Src 0': 'Image Src'}, inplace=True)
    #print(df)
       
    return df
