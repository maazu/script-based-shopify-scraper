import pandas as pd
import requests
import os 
import urllib
import json
from requests.adapters import HTTPAdapter

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
    
#"website_urls3.csv" 



def count_products(csv_file_name):
  df = pd.read_csv(csv_file_name).drop_duplicates(keep='first').reset_index()
  products_count = {}

  
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
  return products_count

csv_file_name = input("Enter the uploaded file name ===========>  ")
csv_file_name = os.getcwd() +"/"+ csv_file_name
print(csv_file_name)

products_count_data = (count_products(csv_file_name))
df = pd.DataFrame(list(products_count_data.items()),columns = ['website','total products']) 
df.sort_values(by=['total products'], inplace=True, ascending=True)
df.to_csv(csv_file_name,index = False, encoding = "utf-8-sig")
