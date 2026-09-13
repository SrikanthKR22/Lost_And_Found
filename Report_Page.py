'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD
from tkinter import filedialog
import os
import shutil

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def report(home_page, report_page, screen):

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
    ).grid(
        row=9,
        column=2,
        padx=(0, 15),
        sticky="w"
    )

     #---#|]========================[FORM-Srt]========================[|#


    #Back Button
    HUD.Label(report_page, text='\n\n\n\n\n\n', bg = 'black').grid(row=15, column=1)
    HUD.Button(report_page, text="Back", command= lambda: go_home(report_page, home_page)).grid(row=16, column=1)

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def go_home(current_page, home_page):
    current_page.grid_remove()
    home_page.grid(row=0, column=0)

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

"""#|/////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""