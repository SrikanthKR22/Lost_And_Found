'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD
import sys
import os
import shutil
import Datalink
import History_Page
import Report_Page
import Search_Page
import View_Reports_Page

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def Quit():
    Datalink.disconnect_datalink()
    if os.path.exists("Temp"):
        shutil.rmtree("Temp")
        os.makedirs("Temp")
    screen.destroy()
    sys.exit()

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#


def toggle_fullscreen(event=None):
    current = screen.attributes('-fullscreen')
    screen.attributes('-fullscreen', not current)

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

class Old_Reports:

    def __init__(self, report_data):
        self.id = report_data[0]
        self.date = report_data[1]
        self.time = report_data[2]
        self.area = report_data[3]
        self.tags = report_data[4].split(", ")
        self.email = report_data[5]
        self.phone = report_data[6]
        self.picture_path = report_data[7]

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def get_old_reports():
    datalink_cursor = Datalink.get_cursor()
    query = "SELECT * FROM Reported_Items"
    datalink_cursor.execute(query)
    your_reports = datalink_cursor.fetchall()
    your_report_objs = []

    for report_data in your_reports:
        your_report_objs.append(Old_Reports(report_data))

    return your_report_objs

your_report_objs = get_old_reports()

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

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
view_reports_page = HUD.Frame(screen)
frame_list = [home_page, report_page, search_page, view_reports_page, history_page, search_result_page]

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
    command= lambda: Report_Page.report(home_page, report_page, view_reports_page, screen),
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
    text= "View Your Reports",
    command= lambda: View_Reports_Page.view_reports(home_page, view_reports_page, screen, your_report_objs),
    font=("Berlin Sans FB Demi", 40),
    bg='black',
    fg = 'cyan'
    ).grid(row=3, column=0, pady=15)

HUD.Button(
    home_page, 
    text= "View history of items found through our App",
    command= lambda: History_Page.history(home_page, history_page, screen),
    font=("Berlin Sans FB Demi", 40),
    bg='black',
    fg = 'orange'
    ).grid(row=4, column=0, pady=(15,50), padx = 50)

HUD.Button(
    home_page,
    text= "Quit",
    command= Quit,
    font= ('Berlin Sans FB Demi', 30),
    bg= 'grey',
    fg= 'white',
).grid(row=5, column=1, padx=(0,25), pady=5)

home_page.grid(row=0, column=0)
screen.mainloop()

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""