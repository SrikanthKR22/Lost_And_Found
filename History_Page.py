'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD
from tkinter import ttk
import Datalink

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def history(home_page, history_page, screen):

    home_page.grid_remove()

    #scaling for maximize
    history_page.grid(row=0, column=0, sticky='nsew')
    history_page.grid_rowconfigure(0, weight=1)
    history_page.grid_columnconfigure(0, weight=1)
    history_page.configure(bg='black')

    #styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("History.Treeview", font=("OCR A Extended", 20), background="black", foreground="white", fieldbackground="black", rowheight=40)
    style.configure("History.Treeview.Heading", font=("Berlin Sans FB Demi", 22, "bold"), background="orange", foreground="black")

    #Back Button
    HUD.Button(history_page, text='Back', command=lambda: go_home(history_page, home_page)).grid(row=1, column=0)

    #fetchign table data
    datalink_cursor = Datalink.get_cursor()
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

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def go_home(current_page, home_page):
    Datalink.disconnect_datalink()
    current_page.grid_remove()
    home_page.grid(row=0, column=0)

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""