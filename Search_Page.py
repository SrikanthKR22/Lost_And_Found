'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD
import Datalink
from datetime import date
import Search_Result_Page

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

def get_all_tags():
    query = "SELECT Desc_Tags FROM Reported_Items"
    datalink_cursor = Datalink.get_cursor()
    datalink_cursor.execute(query)
    all_tags_nested = datalink_cursor.fetchall()
    Datalink.disconnect_datalink()
    all_tags_raw = []
    all_tags = []
    for i in all_tags_nested:
        all_tags_raw.extend(i[0].split())
    for i in all_tags_raw:
        all_tags.append(i.replace(",", "").replace(" ", ""))
    return sorted(set(all_tags))

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def go_home(current_page, home_page):
    current_page.grid_remove()
    home_page.grid(row=0, column=0)

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def search(home_page, search_page, screen):

    class Search_Item:

        def __init__(self, entries):
            self.date = entries['date']
            self.time = entries['time']
            self.area = entries['area']
            self.email = entries['email']
            self.phone = entries['phone']
            self.tags = entries['tags']
            self.other_tags = entries['other_tags']
            self.search_engine()

        #]::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::[#

        @staticmethod
        def get_report_objs():
            query = "SELECT * FROM Reported_Items"
            datalink_cursor = Datalink.get_cursor()
            datalink_cursor.execute(query)
            data = datalink_cursor.fetchall()
            Datalink.disconnect_datalink()
            report_objs = {}

            for row_data in data:
                report_objs[row_data[0]] = Reports(row_data)
            return report_objs

        #]::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::[#

        def search_engine(self):

            report_objs = self.get_report_objs()
            max_match_score = int(bool(self.area)) + len(self.tags) + len(self.other_tags)

            #Date
            for report in report_objs.values():
                if self.date and report.date:
                    if self.date > report.date:
                        report.is_rejected = True

            for report in report_objs.values():

                if not report.is_rejected:

                    report.match_score = 0
                    report.match_percent = 0

                    #Area
                    if (self.area and report.area) and (self.area.strip().lower() == report.area.strip().lower()):
                        report.match_score += 1

                    #Tags
                    for tag_self in self.tags + self.other_tags:
                        if tag_self.strip().lower() in report.tags:
                            report.match_score += 1

                    report.match_percent = (report.match_score/max_match_score) * 100

            self.search_result = list(sorted([report for report in report_objs.values() 
                                            if not report.is_rejected and report.match_percent >= 10], 
                                            key=lambda item: item.match_percent, reverse=True))

            search_result_page = HUD.Frame(screen)
            Search_Result_Page.search_result(home_page, search_result_page, screen, self)       

        #]::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::[#

    class Reports:

        def __init__(self, values):
            self.id = values[0]
            self.date = values[1]
            self.time = values[2]
            self.area = values[3]
            self.tags = values[4].lower().strip().replace(" ", "").split(',')
            self.email = values[5]
            self.phone = values[6]
            self.picture_path = values[7]
            self.is_matched = values[8]
            self.is_rejected = False

        #]::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::[#

    '''#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<CLASS-END>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#'''  

    home_page.grid_remove()

    #Scaling for maximize
    search_page.grid_configure(row=0, column=0, sticky='nsew')
    search_page.grid_columnconfigure(0, weight=1)
    search_page.grid_columnconfigure(1, weight=0)
    search_page.grid_columnconfigure(2, weight=1)
    search_page.grid_rowconfigure(10, weight=3)
    search_page.configure(bg='black')

    #Header
    HUD.Label(search_page, text= "Search For A Lost Item Of Yours", font=("Berlin Sans FB Demi", 25), bg='black', fg= 'red', anchor= 'n').grid(row=0,column=1, padx=20, pady=(20, 50))


    #---#|]========================[FORM-Srt]========================[|#

    #-------#|]=====[Defaults-Srt]=====[|#
    midspace = HUD.Label(search_page, text=' ', font=("OCR A Extended", 18), bg='black', fg='white')

    default_label_dict = {
        'master': search_page,
        'font': ("OCR A Extended", 12),
        'bg': 'black',
        'fg': 'white',
        'anchor': 'w',
        'width': 75
    }

    default_label_grid_dict = {'column': 0, 'padx': (15,0), 'pady': 10}

    default_entry_dict = {
        'master': search_page,
        'font': ("OCR A Extended", 12),
        'bg': 'black',
        'fg': 'white',
        'width': 75
    }

    default_entry_grid_dict = {'column': 2, 'padx': (0,15)}

    #-------#|]=====[Defaults-End]=====[|#

    #Date
    HUD.Label(text="On which date did you find the item (<dd/mm/yy> format, optional): ", **default_label_dict).grid(row=1, **default_label_grid_dict)
    midspace.grid(row=1, column=1)
    date_entry = HUD.Entry(**default_entry_dict)
    date_entry.grid(row=1, **default_entry_grid_dict)

    #Time
    HUD.Label(text="At what time did you find the item (<hh:mm> format, optional): ", **default_label_dict).grid(row=2, **default_label_grid_dict)
    midspace.grid(row=2, column=1)
    time_entry = HUD.Entry(**default_entry_dict)
    time_entry.grid(row=2, **default_entry_grid_dict)

    #Area
    HUD.Label(text="In which area did you find the item (optional): ", **default_label_dict).grid(row=3, **default_label_grid_dict)
    midspace.grid(row=3, column=1)
    area_entry = HUD.Entry(**default_entry_dict)
    area_entry.grid(row=3, **default_entry_grid_dict)

    #Contact
    HUD.Label(text="Enter either [Email] or [Phone Number] or [Both]",**default_label_dict).grid(row=4, **default_label_grid_dict)
    midspace.grid(row=4, column=1)

    #Email
    HUD.Label(text="Enter your email address: ", **default_label_dict).grid(row=5, **default_label_grid_dict)
    midspace.grid(row=5, column=1)
    email_entry = HUD.Entry(**default_entry_dict)
    email_entry.grid(row=5, **default_entry_grid_dict)

    #Phone
    HUD.Label(text="Enter your phone number: ", **default_label_dict).grid(row=6, **default_label_grid_dict)
    midspace.grid(row=6, column=1)
    phone_entry = HUD.Entry(**default_entry_dict)
    phone_entry.grid(row=6, **default_entry_grid_dict)

    #Tags
    HUD.Label(text="Select relevant tags from the existing tags: ", **default_label_dict).grid(row=7, **default_label_grid_dict)
    midspace.grid(row=7, column=1)

    all_tags = get_all_tags()
    tag_listbox = HUD.Listbox(search_page, font=("OCR A Extended", 12), bg='black', fg='white', width=75, height=5, selectmode=HUD.MULTIPLE)
    tag_listbox.insert(HUD.END, *all_tags)
    tag_listbox.grid(row=7, **default_entry_grid_dict)

    #other Tags
    HUD.Label(text="Enter any other relevant tags (comma-separated): ", **default_label_dict).grid(row=8, **default_label_grid_dict)
    midspace.grid(row=8, column=1)
    other_tags_entry = HUD.Entry(**default_entry_dict)
    other_tags_entry.grid(row=8, **default_entry_grid_dict)

    search_entries = {
        "date_entry": date_entry,
        "time_entry": time_entry,
        "area_entry": area_entry,
        "email_entry": email_entry,
        "phone_entry": phone_entry,
        "tag_listbox": tag_listbox,
        "other_tags_entry": other_tags_entry
    }

    #---#|]========================[FORM-End]========================[|#

    #Submit Button
    HUD.Button(search_page, text="Search", command=lambda: submit(search_entries)).grid(row=10, column=2)

    error_label = HUD.Label(
        master=search_page,
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

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Inner-Func]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

    def submit(search_entries):

        #---#|]========================[VALIDATE-Srt]========================[|#

        errors = []
        valid_entries = dict()

        #Date
        date = search_entries["date_entry"].get().strip()
        if date == '':
            date = None
        else:
            try:
                day, month, year = map(int, date.split('/'))
                if len(date.split('/')) != 3 or not (1 <= day <= 31 and 1 <= month <= 12):
                    raise ValueError
                date = f'20{year:02d}-{month:02d}-{day:02d}'
            except ValueError:
                errors.append("Invalid Date!")
        valid_entries['date'] = date

        #Time
        time = search_entries["time_entry"].get().strip()
        if time == '':
            time = None
        else:
            try:
                hour, minute = map(int, time.split(':'))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError
                time = f'{hour:02d}:{minute:02d}:00'
            except ValueError:
                errors.append("Invalid Time!")
        valid_entries['time'] = time

        #Area
        area = search_entries["area_entry"].get().strip()
        area = area if area != '' else None
        valid_entries['area'] = area

        #Email
        email = search_entries["email_entry"].get().strip()
        email = email if email != '' else None
        valid_entries['email'] = email

        #Phone
        phone = search_entries["phone_entry"].get().strip()
        phone = phone if phone != '' else None
        valid_entries['phone'] = phone

        if not (phone or email):
            errors.append("Provide either [Email] or [Phone], or [Both]!")

        #Selected Tags
        selected_tag_indices = search_entries["tag_listbox"].curselection()
        tags = [search_entries["tag_listbox"].get(index) for index in selected_tag_indices]
        valid_entries['tags'] = tags

        #Other Tags
        other_tags = search_entries["other_tags_entry"].get().strip()
        if other_tags == '':
            other_tags = []
        else:
            other_tags = [tag.strip() for tag in other_tags.split(',') if tag.strip()]
        valid_entries['other_tags'] = other_tags

        if not (tags or other_tags):
            errors.append("Provide relevant tags!")


        #---inal send---#
        if errors:
            show_errors(errors)
        else:
            return Search_Item(valid_entries)

        #---#|]========================[VALIDATE-End]========================[|#

    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#
    
    def show_errors(errors):
        error_text = "\n".join(f"• {error}" for error in errors)
        error_label.config(text=error_text)
    
    #]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

    #Back Button
    HUD.Label(search_page, text='\n\n\n\n\n\n', bg = 'black').grid(row=15, column=1)
    HUD.Button(search_page, text="Back", command= lambda: go_home(search_page, home_page)).grid(row=16, column=1)

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""