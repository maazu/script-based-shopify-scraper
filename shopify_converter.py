# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:19:43 2020

@author: Maaz
"""
import os
import requests
import json
import pandas as pd
import re
import time 
import glob
import threading
global summary_dict 
start_time = time.time()
summary_dict = {} 
lock = threading.Lock()
downloading_thread = []
def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


def create_new_directory(location,folder_name):
  
    path = os.path.join(str(location), str(folder_name )+"-"+ str(generated_time()+"/")) 
    os.mkdir(path)
    download_dir = os.path.isdir(path)  
    print(str(folder_name) + "Download directory created: " + str(download_dir))  
    return path



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


def read_website_df_single():  
    csv_file_name = select_csv()
    df = pd.read_csv(csv_file_name).drop_duplicates(keep='first').reset_index()
    return df



def send_requst(url):
    
    try:
        request = requests.get(url, timeout = 5)
        if request.status_code == 200:
            print("Found valid API Endpoint Response code ===> " + str(request.status_code) )
            return True
        else:
            print("API Endpoint Not Found Response code ===> " + str(request.status_code) )
            return False

    except Exception as e:
        print(url, e)
        return False





def check_shopify_store(host_name,store_name):

   if (pd.isnull(host_name) == False):
       page_count = str(1)
       given_storename = "https://" + store_name + "/products.json?limit=250&page="  + page_count
       given_hostname_shop = "https://shop." + host_name + "/products.json?limit=250&page=" + page_count
       given_hostname_store = "https://store." + host_name + "/products.json?limit=250&page=" + page_count
       given_hostname_www = "https://www." + host_name + "/products.json?limit=250&page=" + page_count
       shop_store_name = "https://shop." + store_name + "/products.json?limit=250&page=" + page_count
       store_sore_name = "https://store." + store_name + "/products.json?limit=250&page="+ page_count
       store_name_www = "https://www." + store_name + "/products.json?limit=250&page=" + page_count
      
       request_given_storename = send_requst(given_storename)
       if(request_given_storename == True):
           return given_storename
       
       else: 
           if(given_hostname_shop == True):
               return given_hostname_shop
          
           else:
               if(given_hostname_store == True):
                   return given_hostname_store
          
               else:
                   if(given_hostname_www == True):
                       return given_hostname_www
          
                   else:
                       if(shop_store_name == True):
                           return shop_store_name
          
                       else:
                            if(store_sore_name == True):
                                return store_sore_name
                       
                            else:
                                if(store_name_www == True):
                                    return store_name_www
                                else:
                                    print("All seven attempts failed ===> Adding the url into failed urls ==>" + host_name)
                                    return False
   else:    
       
       print(host_name, "empty url....")
       return False




def check_valid_url(df):
    sucessful_count = 0
    checking_count = 1
    download_dir = create_new_directory("","shopify-data")
    for index, row in df.iterrows():
        
        host_name = str(row['hostname'])
        store_url = str(row['store'])
        valid_url = check_shopify_store(host_name,store_url)
        print(str(checking_count) +"/"+str(len(df))+ "validating "+ store_url +" shopify API endpoint..............")
        if(valid_url != False):
            sucessful_count = sucessful_count + 1 
            valid_url = valid_url[8:-31]
            summary_dict[host_name] = [store_url,valid_url]
            download_thread = threading.Thread(target= start_downloading, args=(download_dir,valid_url,sucessful_count))
            downloading_thread.append(download_thread)
            download_thread.start() 
    
        else:
            summary_dict[host_name] = [store_url,"NOT FOUND"]

        checking_count = checking_count + 1 


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
        print("invalid request")
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
    print("Attempt was made")
    products_records = []
  
    total_products = len(product_json['products'])
    for i in range(0,total_products):
        print("Writing product ==>" +str(i+1))
        product_count = i
      
      
        title = (product_json['products'][product_count]['title'])
        handle = (product_json['products'][product_count]['handle'])
        body_html = (product_json['products'][product_count]['body_html'])
        body_html = re.sub(r"[\n\t\s]*", "", body_html)
        vendor = (product_json['products'][product_count]['vendor'])
        product_type = (product_json['products'][product_count]['product_type'])
        product_tag = (product_json['products'][product_count]['tags'])
        product_tag = ",".join(str(x) for x in product_tag)
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
            
    print("======================================")
   
    fields = ['URL','Handle','Title', 'Body (HTML)','Vendor', 'Type','Tags','Option1 Name','Option1 Value','Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value','Variant Price','Image Src']
    df = pd.DataFrame(products_records,columns = fields)
    df = df.join(df['Image Src'].str.split(',', expand=True).add_prefix('Image Src '))
    df = df.drop('Image Src', 1)
    df.rename(columns={'Image Src 0': 'Image Src'}, inplace=True)
    #print(df)
    return df



def get_json_dump(valid_url):
    try:
        print("Reading url ===> " + valid_url)
        product_json = requests.get(valid_url,timeout = 8).json()
        return product_json
    except Exception as e:
        print(e)
        return False


def start_downloading(download_dir,valid_url,sucessful_count):
    df_list = list()
    next_page = True
    page_count = 0
    web_address = valid_url
    total_products = 0
    while(next_page != False):
        try:
           page_count = page_count + 1
          
           valid_url  = "https://" + valid_url + "/products.json?limit=250&page="+ str(page_count)
           product_json = (get_json_dump(valid_url))
           if(product_json != False):
              
               #print(product_json)
               total_products = len(product_json['products'])
               
               if (total_products < 0 ):
                  print("Reading "+web_address+" Products From Page......" + str(page_count)+ " Total Products Found on Page...." + str(total_products))
                  df = get_products_dataframe(web_address,product_json)
                  df_list.append(df)
                   
               elif (total_products < 250):
                   print("Reading "+web_address+" Products From Page......" + str(page_count)+ " Total Products Found on Page...." + str(total_products))
                   df = get_products_dataframe(web_address,product_json)
                   df_list.append(df)
                   next_page = False
                    
               elif (total_products == 0):
                   print("Reading "+web_address+" Products From Page......" + str(page_count)+ " Total Products Found on Page...." + str(total_products))
                   print("Total Products "+ str(web_address) +"...." + str(total_products))
                   next_page = False
                   break
               
               else:
                 print("Total Products "+ str(web_address) +"...." + str(total_products))
                 next_page = False
                 break

        except Exception as e:
           print(e)
           print("Total Products "+ str(web_address) +"...." + str(total_products))
           next_page = False
           break
    
    
    
    
    if(len(df_list) > 0):
        try:
            
            df = pd.concat(df_list)
            df.to_csv(download_dir+web_address+".csv",index =False, encoding ="utf-8-sig")
            print("Data downloaded sucessfully")
        except Exception as e:
            print(e)
    else:
        print("Empty dataframe found ")
        
  

    


if __name__ == "__main__": 
   
  print("Please upload data and enter batch size")
  batch_size = input("Enter batch size ============>") 
  
  df = (read_website_df_single())
  check_valid_url(df)
 
  df = pd.DataFrame(list(summary_dict.items()),columns = ['hostname','store+validurl']) 
  
  df = df.join(df['store+validurl'].str.split(',', expand=True).add_prefix('Store url '))
  df = df.drop('store+validurl', 1)
  df.rename(columns={'Store url 1': 'Valid Shopify Endpoints'}, inplace=True)
  df.to_csv("urls_test.csv",index =False, encoding ="utf-8-sig")
  print("---Script total time ==> : {0:.3g} seconds ---".format (time.time() - start_time))
  #start_downloading("","pt.business.babbel.com",1)

#-------------------------------------


    
