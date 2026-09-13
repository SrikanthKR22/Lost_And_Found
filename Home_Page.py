'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD
import sys
import Datalink
import History_Page
import Report_Page
import Search_Page

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def Quit():
    Datalink.disconnect_datalink()
    screen.destroy()
    sys.exit()

def toggle_fullscreen(event=None):
    current = screen.attributes('-fullscreen')
    screen.attributes('-fullscreen', not current)

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<MAIN>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

screen = HUD.Tk()

#scaling for maximize
screen.grid_rowconfigure(0, weight=1)
screen.grid_columnconfigure(0, weight=1)
screen.bind('<F11>', toggle_fullscreen)

#Initiating Frames
home_page = HUD.Frame(screen, bg='black')
report_page = HUD.Frame(screen)
search_page = HUD.Frame(screen)
search_result_page = HUD.Frame(screen)
history_page = HUD.Frame(screen)
frame_list = [home_page, report_page, search_page, history_page]

#scaling for maximize
home_page.grid_columnconfigure(0, weight=1)
home_page.grid_rowconfigure(0, weight=1)
home_page.grid_rowconfigure(4, weight=1)
home_page.grid(row=0, column=0, sticky="nsew")


#home_page layout

HUD.Label(
    home_page, text= "LOST AND FOUND",
    font=("Berlin Sans FB Demi", 75),
    bg='black',
    fg= 'orange'
    ).grid(row=0,column=0, padx=50, pady=(20, 75))

HUD.Button(
    home_page,
    text= "Report a Lost Item",
    command= lambda: Report_Page.report(home_page, report_page, screen),
    font=("Berlin Sans FB Demi", 40),
    bg='black',
    fg='green'
    ).grid(row=1, column=0, pady=15)

HUD.Button(
    home_page, text= "Search for a Lost Item of Yours",
    command= lambda: Search_Page.search(home_page, search_page, screen),
    font=("Berlin Sans FB Demi", 40),
    bg='black',
    fg='red'
    ).grid(row=2, column=0, pady=15)

HUD.Button(
    home_page, 
    text= "View history of items found through our App",
    command= lambda: History_Page.history(home_page, history_page, screen),
    font=("Berlin Sans FB Demi", 40),
    bg='black',
    fg = 'orange'
    ).grid(row=3, column=0, pady=(15,50), padx = 50)

HUD.Button(
    home_page,
    text= "Quit",
    command= Quit,
    font= ('Berlin Sans FB Demi', 30),
    bg= 'grey',
    fg= 'white',
).grid(row=4, column=1, padx=(0,25), pady=5)

home_page.grid(row=0, column=0)
screen.mainloop()

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""