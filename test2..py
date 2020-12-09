# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 23:25:13 2020

@author: Acer
"""

import pandas as pd
import asyncio
import aiohttp
from aiohttp import ClientSession, ClientConnectorError


valid_url = {}
invalid_url = {}

def create_shopify_api_endpoint_for_store(url):
    url = "https://" + url + "/products.json?limit=250&page=1"  
    return url


def create_shopify_api_endpoint_for_store_with_www(url):
    url = "https://www." + url + "/products.json?limit=250&page=1"  
    return url

def create_shopify_api_endpoint_for_store_with_http(url):
    url = "http://" + url + "/products.json?limit=250&page=1"  
    return url
    
def get_store_data():
  df=pd.read_csv('reformatted.csv',index_col=False)
  host_name_list = list(df['hostname'])
  store_list = list(df['store'])
  store_list = list(map(create_shopify_api_endpoint_for_store,store_list))
  return [host_name_list,store_list ]   
    

async def update_url_validity_status(validity_status,host,store):
    if(validity_status == "valid"):
        valid_url[host] = store
    else:
        invalid_url[host] = store
    
    print("Total Valid ===> " + str(len(valid_url)))
    print("Total Inalid ===> " + str(len(invalid_url)))
    print("Total Processed ===> " + str(len(valid_url) + len(invalid_url) ))

async def fetch_html(host: str,store: str,count: int, session: ClientSession, **kwargs) -> tuple:
    try:
        response = await session.request(method="GET", url=store, **kwargs)
        await response.read()
        
        status = response.status
        contentType = response.headers.get('content-type')
        
        if (status == 200 and contentType == "application/json" or status == 200 and contentType == "application/json; charset=utf-8"):
            print(str(count)+ " Valid")
            await update_url_validity_status("valid",host,store)
            return True
        else:
            print(str(count)+ "Invalid")
            await update_url_validity_status("invalid",host,store)
            return False
            
    except Exception as e:
        print(e)
        store_url = store[8:-31]
        store = create_shopify_api_endpoint_for_store_with_www(store)
        if(fetch_html(host = host, store = store, count = count, session=session, **kwargs) == True):
            pass
        else:
             store_url = store[8:-31]
             store =  create_shopify_api_endpoint_for_store_with_http(store)
          
             if(fetch_html(host = host, store = store, count = count, session=session, **kwargs) == True):
                 
                 pass
             else:
                 print(str(count)+ "Invalid")
                 await update_url_validity_status("invalid",host,store)
                 return False
    

async def make_requests(host_name_list: list, store_name_list: list, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        count = 0 
        for host,store in zip(host_name_list,store_name_list):
            
            tasks.append(
                fetch_html(host = host, store = store, count = count, session=session, **kwargs)
            )
            count = count +  1
        results = await asyncio.gather(*tasks)

    for result in results:
        print(f'{result[1]} - {str(result[0])}')




if __name__ == "__main__":
    
   host_name_list = get_store_data()[0]
   store_name_list = get_store_data()[1]
   asyncio.run(make_requests(host_name_list,store_name_list))