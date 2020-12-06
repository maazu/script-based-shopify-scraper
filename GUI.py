from tkinter import *
from validation import *

from testing import  *
class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.title('Shopify | Scrapper ')
        self.root.resizable(False, False)
        self.root.geometry('1000x700')

        frame = Frame(self.root)
        frame.pack()
        self.root.update()
        #left frame  - MENU SIDE

        leftframe = Frame(self.root,bg ='#001f42')
        leftframe.pack(side = LEFT)
        leftframe.place(height=800, width=280, x=0, y=0)

        #right frame - DISPAY SIDE
        rightframe = Frame(self.root,bg='#003e85')
        rightframe.pack(side = RIGHT)
        rightframe.place(height=800, width=800, x=200, y=0)


        #Project Logo
        project_logo = Label(leftframe, text=" Shopify \nthe real scraper", font=("Helvetica", 16),bg='#001f42',fg = 'WHITE')
        project_logo.place(x=35, y=20)

        #Footer Note
        footer_note = Label(leftframe, text=" Developed  by \n Muhammad Maaz\n For by: Mr Da \n", font=("Helvetica", 8),bg='#001f42',fg = 'WHITE')
        footer_note.place(x=0, y=600)


        #Server Button
        #Server_button = Button(leftframe, text="Server", fg="black", width = 20, command= lambda:server_page(self))
        #Server_button.place(x=25, y=150)

        #Validate urls

        validate_page_button = Button(leftframe, text="Validation", fg="black", width = 20,command = lambda:validation_urls_page(self))
        validate_page_button.place(x=25, y=200)

        #Product counting button
        products_counting_page_button = Button(leftframe, text="Products Counting", fg="black", width = 20,command = lambda:name_of_function(self))
        products_counting_page_button.place(x=25, y=250)



        #Download CSV Button
        download_csv_button = Button(leftframe, text="Download csv", fg="black", width = 20, command = lambda:name_of_function(self))
        download_csv_button.place(x=25, y=300)



        Quit_button = Button(leftframe, text="Quit", fg="black", width = 20,command=self.quit_page)
        Quit_button.place(x=25, y=350)




    def map_page(self):

        self.root.update()
        rightframe = Frame(self.root,bg='black')
        rightframe.pack(side = RIGHT)
        rightframe.place(height=800, width=800, x=200, y=0)
        project_logo = Label(rightframe, text="Map View", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
        project_logo.place(x=35, y=20)



    def quit_page(self):

        self.root.update()
        rightframe = Frame(self.root,bg='black')
        rightframe.pack(side = RIGHT)
        rightframe.place(height=800, width=800, x=200, y=0)
        quit_heading = Label(rightframe, text="Quit", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
        quit_heading.place(x=35, y=20)

        quit_note = "Pressing Yes button will shut the entirely."
        quit_heading = Label(rightframe, text=quit_note, font=("Helvetica", 11),bg ='black',fg = 'WHITE')
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
