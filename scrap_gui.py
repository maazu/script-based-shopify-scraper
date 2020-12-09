# -*- coding: utf-8 -*-

"""
Created on Mon Dec  7 18:19:06 2020

@author: Maaz
"""
import os
from tkinter import *
from reformat_page import *
from validation_page import *
from PIL import Image, ImageTk
rightframe_background_color = "#EDE9D8"  #light grey


standard_font_name = "Motiva Sans"
rightframe_background_color = "#EDE9D8"
foreground_color = "#173630"
font_weight ="bold"
button_background_color = "#108043"
text_font_size = 12

class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Shopify | Scraper ')
        self.root.resizable(False, False)
        self.root.geometry('1000x700')
        
        frame = Frame(self.root)  
        frame.pack()  
        self.root.update() 
        #left frame  - MENU SIDE

        leftframe = Frame(self.root,bg ='#F4F6F8')  
        leftframe.pack(side = LEFT)  
        leftframe.place(height=800, width=280, x=0, y=0)

        #right frame - DISPAY SIDE
        rightframe = Frame(self.root,bg= rightframe_background_color)  
        rightframe.pack(side = RIGHT)  
        rightframe.place(height=800, width=800, x=200, y=0)

        
        #Project Logo
        load = Image.open( os.getcwd() + "/imgs/logo.png")
        render = ImageTk.PhotoImage(load) 
        img = Label(leftframe, image=render)
        img.image = render
        img.place(x=35, y=20)   
        
        project_logo = Label(leftframe, text="data extractor", font=("Motiva Sans",14, "bold","italic"), bg='#F4F6F8',fg = 'black')
        project_logo.place(x=53, y=80)
        
        #reformat Button
        reformat_button = Button(leftframe, text="Reformat", bg="#108043" ,fg="white", width = 20,command = lambda:reformat_dataset(self,"reformat-data"))  
        reformat_button.place(x=25, y=200)
        
        validation_button = Button(leftframe, text="Validate",bg="#108043" , fg="white", width = 20,command = lambda:validate_dataset(self,"validate-data"))  
        validation_button.place(x=25, y=250)

        count_button = Button(leftframe, text="Counting",bg="#108043" , fg="white", width = 20,command = lambda:validate_dataset(self,"validate-data"))  
        count_button.place(x=25, y=300)
        
        download_button = Button(leftframe, text="Download",bg="#108043" , fg="white", width = 20,command = lambda:validate_dataset(self,"validate-data"))  
        download_button.place(x=25, y=350)
        
        
        quit_button = Button(leftframe, text="Quit", bg="#108043" , fg="white", width = 20,command=self.quit_page)  
        quit_button.place(x=25, y=400)



        
    def quit_page(self):
        self.root.update() 
        rightframe = Frame(self.root,bg = rightframe_background_color)  
        rightframe.pack(side = RIGHT)  
        rightframe.place(height=800, width=800, x=200, y=0)
        quit_heading = Label(rightframe, text="Quit", font=(standard_font_name, text_font_size,font_weight),bg = rightframe_background_color,fg = foreground_color)
        quit_heading.place(x=35, y=20)

        quit_note = "Pressing Yes button will shut the entirely."
        quit_heading = Label(rightframe, text=quit_note, font=(standard_font_name, text_font_size,font_weight),bg = rightframe_background_color,fg = foreground_color)
        quit_heading.place(x=35, y=50)
        quit_button = Button(rightframe, text="Yes", fg="black", width = 20,command=lambda:quit_program())  
        quit_button.place(x=35, y=100)


    
    def start(self):
        self.root.mainloop()




def quit_program():
    print("Closing program")
    exit(0) 
    
    
    
         
if __name__ == "__main__":  
    appstart = GUI()
    appstart.start()
   