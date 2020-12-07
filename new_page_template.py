# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:26:54 2020

@author: Acer
"""
import time 
import os
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
from tkinter import ttk 
import pandas as pd

from threading import Thread
from tkinter import messagebox as mbox



def new_page_template(self):
    self.root.update()
    global rightframe
    rightframe = Frame(self.root,bg='black')  
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)