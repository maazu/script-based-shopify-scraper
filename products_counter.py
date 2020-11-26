import pandas as pd
import requests
import os 
import urllib
import json
from requests.adapters import HTTPAdapter
import glob
import time
def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


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



def check_valid_domain(url):
    
    if (pd.isnull(url) == False):
      try:
          request = requests.get("https://www."+ url)
          #print("https://www."+url)
          if request.status_code == 200:
            return True
          else:
              print(url, 'Web site fetching error', request.status_code) 
              return False
      except requests.exceptions.ConnectionError as e:
          print(url, "Connection blocked !", e)
          return False
      else:
           print(url, "empty url....")
           return False


def get_json_data_frame(web_address,page_number):
    
    try:
        url = "https://www."+web_address+"/products.json?limit=250&page"+str(page_number)
        with urllib.request.urlopen("https://www."+web_address+"/products.json?limit=250&page="+str(page_number)) as url:
            data = json.loads(url.read().decode())
            return data
    except Exception as e:
      print(str(url) + "url not found" + str(e))
      data = 404
      return data
    
    
def count_products(csv_file_name):
  
  df = pd.read_csv(csv_file_name).drop_duplicates(keep='first').reset_index()
  products_count = {}
  failed_urls = list()
  failded_df = pd.DataFrame(columns = ['Failed_URL'])
  
  for index, row in df.iterrows():
    web_address = str(row['website'])
    if (check_valid_domain(web_address) == True):
      next_page = True
      page_count = 0
      product_count = 0
      while(next_page != False):
        try:
           page_count = page_count + 1
           products_dict = (get_json_data_frame(web_address,page_count))
           products_df = pd.DataFrame(products_dict)
           total_productsf = len(products_df)
          
           if (total_productsf != 0 ):
   
              product_count = product_count + total_productsf
              
              #print("Reading "+web_address+" Products From Page......" + str(page_count)+ " Total Products Found on Page...." + str(total_productsf))
              if (web_address in products_count):
                products_count[web_address] += total_productsf
                #print(products_count[web_address])
              else:
                products_count[web_address] = total_productsf
                #print(products_count[web_address])
           
           elif (total_productsf == 0 ):
                print("Total Products "+ str(web_address) +"...." + str(product_count))
                next_page = False
                break
           
           else:
             print("Total Products "+ str(web_address) +"...." + str(product_count))
             next_page = False
             break

        except:
           print("Total Products "+ str(web_address) +"...." + str(product_count))
           next_page = False
           break

  failded_df['Failed_URL'] =  pd.Series(failed_urls)  
  failded_df.to_csv("Failed-URL-"+ str(generated_time())+".csv", encoding='utf-8-sig' ,index=False)    
  return products_count

if __name__ == "__main__":  
    csv_file_name = select_csv()
    total_product_dict = count_products(csv_file_name)
    df = pd.DataFrame(list(products_count_data.items()),columns = ['website','total products']) 
    df.sort_values(by=['total products'], inplace=True, ascending=True)
    df.to_csv("/content/sorted_dataset"+generated_time()+".csv",index = False, encoding = "utf-8-sig")
