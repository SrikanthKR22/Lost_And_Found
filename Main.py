
#\=________________________________imports________________________________/=#

import tkinter as HUD
from tkinter import ttk
import datalinnk_Connector
import re

#\=________________________________functions________________________________/=#


def report():

    home_page.grid_remove()

    #Scaling for maximize
    report_page.grid_configure(row=0, column=0, sticky='nsew')
    report_page.grid_columnconfigure(1, weight=3)
    report_page.grid_columnconfigure(2, weight=4)
    report_page.grid_rowconfigure(10, weight=3)
    report_page.configure(bg='black')

    #Header
    HUD.Label(report_page, text= "Report Found Item", font=("Berlin Sans FB Demi", 25), bg='black', fg= 'orange', anchor= 'n').grid(row=0,column=1, padx=20, pady=(0, 50))

    #|------------FORM-Srt------------|#

    #|---Defaults-Srt---|#
    midspace = HUD.Label(report_page, text = ' ', font=("OCR A Extended", 18), bg='black', fg='white',)

    default_label_dict = {
        'master': report_page,
        'font': ("OCR A Extended", 12),
        'bg': 'black',
        'fg': 'white',
        'anchor': 'w',
        'width' : 75
    }

    default_label_grid_dict = {
        'column': 0,
        'padx': (15,0),
        'pady': 10
    }

    default_entry_dict = {
        'master': report_page,
        'font': ("OCR A Extended", 12),
        'bg': 'black',
        'fg': 'white',
        #'anchor' : 'e',
        'width' : 75
    }

    default_entry_grid_dict = {
        'column': 2,
        'padx': (0,15)
    }

    #|---Defaults-End---|#

    #Date
    HUD.Label(text="On which date did you find the item (<dd/mm/yy> format): ", **default_label_dict).grid(row=1, **default_label_grid_dict)
    midspace.grid(row=1, column=1)
    date_entry = HUD.Entry(**default_entry_dict)
    date_entry.grid(row=1, **default_entry_grid_dict)


    #Time
    HUD.Label(text="At what time did you find the item (<hh:mm> format): ", **default_label_dict).grid(row=2, **default_label_grid_dict)
    midspace.grid(row=2, column=1)
    time_entry = HUD.Entry(**default_entry_dict)
    time_entry.grid(row=2, **default_entry_grid_dict)

    #Area
    HUD.Label(text="In which area did you find the item: ", **default_label_dict).grid(row=3, **default_label_grid_dict)
    midspace.grid(row=3, column=1)
    area_entry = HUD.Entry(**default_entry_dict)
    area_entry.grid(row=3, **default_entry_grid_dict)

    #Desc_Tags
    HUD.Label(text="Describe item using relevant tags (like: <colour>, <brand>,...): ", **default_label_dict).grid(row=4, **default_label_grid_dict)
    midspace.grid(row=4, column=1)
    desc_tags_entry = HUD.Entry(**default_entry_dict)
    desc_tags_entry.grid(row=4, **default_entry_grid_dict)

    #Contact
    HUD.Label(text="Enter either [Email] or [Phone Number] or [Both]",**default_label_dict).grid(row=5, **default_label_grid_dict)
    midspace.grid(row=5, column=1)

    #Email
    HUD.Label(text="Enter your email address: ",**default_label_dict).grid(row=6, **default_label_grid_dict)
    midspace.grid(row=6, column=1)
    email_entry = HUD.Entry(**default_entry_dict)
    email_entry.grid(row=6, **default_entry_grid_dict)

    #Phone
    HUD.Label(text="Enter your phone number: ",**default_label_dict).grid(row=7, **default_label_grid_dict)
    midspace.grid(row=7, column=1)
    phone_entry = HUD.Entry(**default_entry_dict)
    phone_entry.grid(row=7, **default_entry_grid_dict)

    #|------------FORM-End------------|#


    #Back Button
    HUD.Label(report_page, text='\n\n\n\n\n\n', bg = 'black').grid(row=10, column=1)
    HUD.Button(report_page, text="Back", command= lambda: go_home(report_page)).grid(row=11, column=1)

    #\==--------Func-End--------==/#

def search():

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
    HUD.Button(search_page, text="Back", command= lambda: go_home(search_page), anchor='s').grid(row=15, column=1)

    #\==--------Func-End--------==/#

def history():

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
    HUD.Button(history_page, text='Back', command=lambda: go_home(history_page)).grid(row=1, column=0)

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

def go_home(current_page):
    current_page.grid_remove()
    home_page.grid(row=0, column=0)

    #\==--------Func-End--------==/#

    #\==--------Form-Validators--------==/#

    def _isvalid_date(date_entry):
        if isinstance(date_entry, str):
            date_entry = date_entry.strip()
            match = re.fullmatch('(0[1-9]|[10-31])/(0[1-9]|11|12)/(2[6-9]|[3-9][0-9])', date_entry)
            if match:
                int_date = int(match.group(1))
                int_month = (match.group(2))
                int_year = (match.group(3))
            
                if ((int_year % 4 == 0) and int_month == 2 and int_date > 29) or (int_month == 2 and int_date > 28):
                    return False

                if int_month in [4,6,9,11] and int_date > 30:
                    return False
                return True

            else:
                return False
            
        else:
            return False

    #\==--------Func-End--------==/#

    def _isvalid_time(time_entry):
        if isinstance(time_entry, str):
            time_entry = time_entry.strip()
            match = re.fullmatch('(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])', time_entry)

            if match:
                return True
            else:
                return False

        else:
            return False


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
frame_list = [home_page, report_page, search_page, history_page]

#HomepageLayout
HUD.Label(home_page, text= "LOST AND FOUND", font=("Berlin Sans FB Demi", 75), bg='black', fg= 'orange').grid(row=0,column=0, padx=50, pady=(20, 75))
HUD.Button(home_page, text= "Report a Lost Item", command= report, font=("Berlin Sans FB Demi", 40), bg='black', fg='green').grid(row=1, column=0, pady=15)
HUD.Button(home_page, text= "Search for a Lost Item of Yours", command= search, font=("Berlin Sans FB Demi", 40), bg='black', fg='red').grid(row=2, column=0, pady=15)
HUD.Button(home_page, text= "View history of items found through our App", command= history, font=("Berlin Sans FB Demi", 40), bg='black', fg = 'orange').grid(row=3, column=0, pady=(15,50), padx = 50)

home_page.grid(row=0, column=0)
screen.mainloop()

#\=________________________________end________________________________/=#