
#\=____________________imports____________________/=#

import tkinter as HUD
from tkinter import ttk
import datalinnk_Connector

#\=____________________functions____________________/=#

def report():
    print("Lets Report!")

def search():
    print('Lets Search!')

def history():

    home_page.grid_remove()
    history_page.grid(row=0, column=0)
    HUD.Button(history_page, text='Back', command=go_home).grid(row=1, column=0)

    datalink_cursor = datalinnk_Connector.get_cursor()
    datalink_cursor.execute("SELECT * FROM List_Of_Found_Items")
    history_view = datalink_cursor.fetchall()
    table = ttk.Treeview(
        history_page,
        columns=('Id', 'Date', 'Time', 'Date_Returned', 'Time_Returned'),
        show="headings"
    )
    table.heading("Id", text="ID")
    table.heading("Date", text="Found Date")
    table.heading("Time", text="Found Time")
    table.heading("Date_Returned", text="Returned Date")
    table.heading("Time_Returned", text="Returned Time")

    for row in history_view:
        table.insert('', 'end', values=row)
    table.grid(row=0, column=0)

def go_home():
    history_page.grid_remove()
    home_page.grid(row=0, column=0)

#\=____________________main____________________/=#

screen = HUD.Tk()
home_page = HUD.Frame(screen)
report_page = HUD.Frame(screen)
search_page = HUD.Frame(screen)
search_result_page = HUD.Frame(screen)
history_page = HUD.Frame(screen)

HUD.Label(home_page, text= "LOST AND FOUND").grid(row=0,column=0)

HUD.Button(home_page, text= "Report a Lost Item", command= report).grid(row=1, column=0)
HUD.Button(home_page, text= "Search for a Lost Item of Yours", command= search).grid(row=2, column=0)
HUD.Button(home_page, text= "View history of items found through our App", command= history).grid(row=3, column=0)

home_page.grid(row=0, column=0)
screen.mainloop()

#\=____________________end____________________/=#