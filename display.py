import tkinter
from tkinter import *
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox

from validate_urls import *

# global  rightframe
# global fvalidation_dataset_path

rightframe = ''
fvalidation_dataset_path = 0
def page_refresh(self,validation_dataset_path):
    global rightframe
    global fvalidation_dataset_path
    self.root.update()
    rightframe = Frame(self.root,bg='white')
    rightframe.pack(side = RIGHT)
    rightframe.place(height=800, width=800, x=200, y=0)


    self.root.update()
    df =  read_website_df_single(validation_dataset_path)
    host_name_list = list(df['hostname'])
    store_list = list(df['store'].apply(create_shopify_api_endpoint_for_store))

    test()
