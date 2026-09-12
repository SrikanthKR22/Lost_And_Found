
#\=________________________________imports________________________________/=#

import tkinter as HUD
from tkinter import ttk
import datalinnk_Connector

#\=________________________________functions________________________________/=#


def report():
    print("Lets Report!")

    #\==--------Func-End--------==/#

def search():
    print('Lets Search!')

    #\==--------Func-End--------==/#

def history():

    home_page.grid_remove()
    history_page.grid(row=0, column=0, sticky='nsew')

    #scaling for maximize
    history_page.grid_rowconfigure(0, weight=1)
    history_page.grid_columnconfigure(0, weight=1)
    history_page.configure(bg='black')

    #styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("History.Treeview", font=("OCR A Extended", 20), background="black", foreground="white", fieldbackground="black", rowheight=40)
    style.configure("History.Treeview.Heading", font=("Berlin Sans FB Demi", 22, "bold"), background="orange", foreground="black")

    #back Button
    HUD.Button(history_page, text='Back', command=go_home).grid(row=1, column=0)

    #fetchign table data
    datalink_cursor = datalinnk_Connector.get_cursor()
    datalink_cursor.execute("SELECT * FROM List_Of_Found_Items")
    history_view = datalink_cursor.fetchall()
    table = ttk.Treeview(
        history_page,
        columns=('Id', 'Date', 'Time', 'Date_Returned', 'Time_Returned'),
        show="headings",
        style="History.Treeview"
    )

    table.column("Id", anchor="center")
    table.column("Date", anchor="center")
    table.column("Time", anchor="center")
    table.column("Date_Returned", anchor="center")
    table.column("Time_Returned", anchor="center")
    table.heading("Id", text="ID")
    table.heading("Date", text="Found Date")
    table.heading("Time", text="Found Time")
    table.heading("Date_Returned", text="Returned Date")
    table.heading("Time_Returned", text="Returned Time")

    #printing Table
    for row in history_view:
        table.insert('', 'end', values=row)
    table.grid(row=0, column=0, sticky="nsew")

    #\==--------Func-End--------==/#

def go_home():
    history_page.grid_remove()
    home_page.grid(row=0, column=0)

    #\==--------Func-End--------==/#


#\=________________________________main________________________________/=#

screen = HUD.Tk()
#scaling for maximize
screen.grid_rowconfigure(0, weight=1)
screen.grid_columnconfigure(0, weight=1)

#Homepage rame __init__
home_page = HUD.Frame(screen, bg='black')

#scaling for maximize
home_page.grid_columnconfigure(0, weight=1)
home_page.grid_rowconfigure(0, weight=1)
home_page.grid_rowconfigure(4, weight=1)
home_page.grid(row=0, column=0, sticky="nsew")

#Frames for pages
report_page = HUD.Frame(screen)
search_page = HUD.Frame(screen)
search_result_page = HUD.Frame(screen)
history_page = HUD.Frame(screen)

#HomepageLayout
HUD.Label(home_page, text= "LOST AND FOUND", font=("Berlin Sans FB Demi", 75), bg='black', fg= 'orange').grid(row=0,column=0, padx=50, pady=(20, 75))
home_page.grid_rowconfigure(1, minsize=30) #spacing
HUD.Button(home_page, text= "Report a Lost Item", command= report, font=("Berlin Sans FB Demi", 40), bg='black', fg='green').grid(row=1, column=0, pady=15)
HUD.Button(home_page, text= "Search for a Lost Item of Yours", command= search, font=("Berlin Sans FB Demi", 40), bg='black', fg='red').grid(row=2, column=0, pady=15)
HUD.Button(home_page, text= "View history of items found through our App", command= history, font=("Berlin Sans FB Demi", 40), bg='black', fg = 'orange').grid(row=3, column=0, pady=(15,50), padx = 50)

home_page.grid(row=0, column=0)
screen.mainloop()

#\=________________________________end________________________________/=#