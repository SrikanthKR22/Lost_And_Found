'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def search(home_page, search_page, screen):

    home_page.grid_remove()

    #Scaling for maximize
    search_page.grid_configure(row=0, column=0, sticky='nsew')
    search_page.grid_rowconfigure(0,weight=1)
    search_page.grid_columnconfigure(0, weight=1)
    search_page.configure(bg='black')

    #Header
    HUD.Label(search_page, text= "Search For Lost Item", font=("Berlin Sans FB Demi", 50), bg='black', fg= 'orange').grid(row=0,column=1, padx=50, pady=(20, 50))
    midspace = HUD.Label(search_page, text = ' ', font=("OCR A Extended", 20), bg='black', fg='white')

    #Back Button
    HUD.Button(search_page, text="Back", command= lambda: go_home(search_page, home_page), anchor='s').grid(row=15, column=1)

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def go_home(current_page, home_page):
    current_page.grid_remove()
    home_page.grid(row=0, column=0)

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""