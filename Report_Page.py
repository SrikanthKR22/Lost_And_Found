'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import Datalink
import tkinter as HUD
from tkinter import filedialog
import os
import shutil
import re
from datetime import date
import View_Reports_Page

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def report(home_page, report_page, view_reports_page, screen):

    #|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<CLASS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

    class Reported_Item():

        def __init__(self, entries):

            self.date = entries['date_entry']
            self.time = entries['time_entry']
            self.area = entries['area_entry']
            self.tags = entries['desc_tags_entry']
            self.email = entries['email_entry']
            self.phone = entries['phone_entry']
            self.picture_path = entries['picture_path']

            date_sql = f"20{self.date[2]:02d}-{self.date[1]:02d}-{self.date[0]:02d}"
            time_sql = f"{self.time[0]:02d}:{self.time[1]:02d}:00"

            insert_query = """
                INSERT INTO Reported_Items
                (Date, Time, Area, Desc_Tags, Email, Phone, Picture_Path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            insert_values = (
                date_sql,
                time_sql,
                self.area,
                ", ".join(self.tags),
                self.email if self.email else None,
                self.phone if self.phone else None,
                self.picture_path
            )

            cursor = Datalink.get_cursor()
            cursor.execute(insert_query, insert_values)

            self.id = cursor.lastrowid

            # ---------------- MOVE PICTURE ----------------

            os.makedirs("Pictures", exist_ok=True)
            old_name = os.path.basename(self.picture_path)
            new_name = f"{self.id}_{old_name}"
            new_path = os.path.join("Pictures", new_name)
            shutil.move(self.picture_path, new_path)
            self.picture_path = new_path

            # ---------------- UPDATE PICTURE PATH ----------------

            update_query = """
                UPDATE Reported_Items
                SET Picture_Path = %s
                WHERE Id = %s
            """

            cursor.execute(update_query,(self.picture_path, self.id))
            Datalink.commit()
            Datalink.disconnect_datalink
            report_page.grid_remove()

        @classmethod
        def from_database(cls, report):
            obj = cls.__new__(cls)
            obj.id = report[0]
            obj.date = report[1]
            obj.time = report[2]
            obj.area = report[3]
            obj.tags = report[4].split(", ")
            obj.email = report[5]
            obj.phone = report[6]
            obj.picture_path = report[7]
            return obj

    '''#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<CLASS-END>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#'''  

    #settign up old reports
    def get_old_reports():
        datalink_cursor = Datalink.get_cursor()
        query = "SELECT * FROM Reported_Items"
        datalink_cursor.execute(query)
        your_reports = datalink_cursor.fetchall()
        your_report_objs = []

        for report_data in your_reports:
            your_report_objs.append(Reported_Item.from_database(report_data))

        return your_report_objs

    your_report_objs = get_old_reports()

    #bring in the report_page
    home_page.grid_remove()

    #Scaling for maximize
    report_page.grid_configure(row=0, column=0, sticky='nsew')
    report_page.grid_columnconfigure(0, weight=1)
    report_page.grid_columnconfigure(1, weight=0)
    report_page.grid_columnconfigure(2, weight=1)
    report_page.grid_rowconfigure(10, weight=3)
    report_page.configure(bg='black')

    #Header
    HUD.Label(report_page, text= "Report Found Item", font=("Berlin Sans FB Demi", 25), bg='black', fg= 'orange', anchor= 'n').grid(row=0,column=1, padx=20, pady=(0, 50))

    #---#|]========================[FORM-Srt]========================[|#

    #-------#|]=====[Defaults-Srt]=====[|#
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
        'width' : 75
    }

    default_entry_grid_dict = {
        'column': 2,
        'padx': (0,15)
    }

    #-------#|]=====[Defaults-End]=====[|#

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
    HUD.Label(text="Describe item using relevant coma-separated tags: ", **default_label_dict).grid(row=4, **default_label_grid_dict)
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

    #Picture
    picture_path = HUD.StringVar()

    def choose_picture():
        selected_path = filedialog.askopenfilename(
            title="Select Item Picture",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.gif"),
                ("All Files", "*.*")
            ])
        if selected_path:
            os.makedirs("Temp", exist_ok=True)
            file_name = os.path.basename(selected_path)
            destination = os.path.join("Temp", file_name)
            shutil.copy2(selected_path, destination)
            picture_path.set(destination)

    HUD.Label(
        text="Picture of found item:",
        **default_label_dict
    ).grid(row=8, column=0, padx=(15, 0), pady=10)
    midspace.grid(row=8, column=1)

    HUD.Button(
        master= report_page,
        text="Choose Picture",
        command=choose_picture
    ).grid(row=8, column=2, padx=(0, 15))

    HUD.Label(
        master= report_page,
        textvariable=picture_path,
        font=("OCR A Extended", 10),
        bg="black",
        fg="white",
        anchor="w"
    ).grid(row=9, column=2, padx=(0, 15), sticky="w")

    #logging values and submit button
    entries = dict()
    entries['date_entry'] = date_entry
    entries['time_entry'] = time_entry
    entries['area_entry'] = area_entry
    entries['desc_tags_entry'] = desc_tags_entry
    entries['email_entry'] = email_entry
    entries['phone_entry'] = phone_entry
    entries['picture_path'] = picture_path

    HUD.Button(
        master=report_page,
        text="Submit",
        command=lambda: submit(entries)
    ).grid(row=10, column=2, padx=20, pady=20)

    error_label = HUD.Label(
        master=report_page,
        text="",
        font=("OCR A Extended", 11),
        bg="black",
        fg="red",
        justify="left",
        anchor="w"
    )

    error_label.grid(
        row=17,
        column=1,
        columnspan=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    def show_errors(errors):
        error_text = "\n".join(f"• {error}" for error in errors)
        error_label.config(text=error_text)

    #---#|]========================[FORM-End]========================[|#


    #Back Button
    HUD.Label(report_page, text='\n\n\n\n\n\n', bg = 'black').grid(row=15, column=1)
    HUD.Button(report_page, text="Back", command= lambda: go_home(report_page, home_page)).grid(row=16, column=1)

    def submit(entries):

        errors = []
        valid_entries = {}

        # ---------------- DATE ----------------

        date_result = _isvalid_date(entries['date_entry'].get())

        if date_result is None:
            errors.append("Invalid date")
        else:
            valid_entries['date_entry'] = date_result

        # ---------------- TIME ----------------

        time_result = _isvalid_time(entries['time_entry'].get())

        if time_result is None:
            errors.append("Invalid time")
        else:
            valid_entries['time_entry'] = time_result

        # ---------------- AREA ----------------

        area = entries['area_entry'].get().strip()

        if not area:
            errors.append("Invalid area")
        else:
            valid_entries['area_entry'] = area

        # ---------------- TAGS ----------------

        tags = [
            tag.strip()
            for tag in entries['desc_tags_entry'].get().split(',')
            if tag.strip()
        ]

        if not tags:
            errors.append("Invalid description/tags")
        else:
            valid_entries['desc_tags_entry'] = tags

        # ---------------- CONTACT ----------------

        email = entries['email_entry'].get().strip()
        phone = entries['phone_entry'].get().strip()

        if not email and not phone:
            errors.append("Enter either an email address or phone number")
        else:
            valid_entries['email_entry'] = email
            valid_entries['phone_entry'] = phone

        # ---------------- PICTURE ----------------

        picture_path = entries['picture_path'].get()

        if not picture_path:
            errors.append("No picture selected")
        else:
            valid_entries['picture_path'] = picture_path

        # ---------------- RESULT ----------------

        if errors:
            show_errors(errors)
            return
        else:
            show_errors(['Form Submitted!'] + list(valid_entries.values()))

        your_report_objs.append(Reported_Item(valid_entries))
        View_Reports_Page.view_reports(home_page, view_reports_page, screen, your_report_objs)
        return

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def go_home(current_page, home_page):
    current_page.grid_remove()
    home_page.grid(row=0, column=0)

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def _isvalid_date(date_entry):

    date_entry = date_entry.strip()
    match = re.fullmatch(r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{2})', date_entry)
    if not match:
        return None
    
    day = int(match.group(1))
    month = int(match.group(2))
    year = int(match.group(3))

    #february
    if month == 2:
        leap_year = (year % 4 == 0)
        if leap_year and day > 29:
            return None
        if not leap_year and day > 28:
            return None

    #30-day months
    if month in [4, 6, 9, 11] and day > 30:
        return None

    #block future dates
    full_year = 2000 + year
    given_date = date(full_year, month, day)
    if given_date > date.today(): 
        return None 

    return [day, month, year]

#]:::::::::::::::::::[Func-End]:::::::::::::::::::[#

def _isvalid_time(time_entry):
    time_entry = time_entry.strip()
    match = re.fullmatch(r'(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])', time_entry)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2))
    return [hour, minute]
    
#]:::::::::::::::::::[Func-End]:::::::::::::::::::[#


"""#|/////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""