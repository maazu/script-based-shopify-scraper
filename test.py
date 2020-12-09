# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:30:30 2020

@author: Acer
"""
import time
import random
import asyncio
from aiohttp import ClientSession
data_dic = {}
error_dict = {}

async def update_dictonary(url):
    
    


async def fetch(url, session):
    async with session.get(url) as response:
        await response.read()
        delay = response.headers.get("DELAY")
        date = response.headers.get("DATE")
      
        fetched_json = await response.json()
        
        if 'products' in fetched_json:
            sucess_dict[url] = response.url
        else:
            error_dict = {}
       


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r):
    url = "https://www.rooneyshop.com/products.json?limit=250&page={}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(1,r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
            print( url.format(i))
            time.sleep(0.10)
            tasks.append(task)
            print("return data =========>" )
            print(task)
        responses = asyncio.gather(*tasks)
        await responses
       
    return responses
    
    
    
number = 5
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)

print(loop)