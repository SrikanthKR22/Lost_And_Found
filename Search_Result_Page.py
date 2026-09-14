'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

import tkinter as HUD
import Datalink
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


def go_home(current_page, home_page):
    current_page.grid_remove()
    home_page.grid(row=0, column=0)


def found_item(button, Id):

    datalink_cursor = Datalink.get_cursor()

    #Check whether reporter has marked the item as matched
    get_query = """
    SELECT is_matched
    FROM Reported_Items
    WHERE Id = %s
    """

    datalink_cursor.execute(get_query, (Id,))
    result = datalink_cursor.fetchone()

    if result is None:
        Datalink.disconnect_datalink()
        return

    if not result[0]:
        Datalink.disconnect_datalink()
        return

    #Mark item as alloted
    set_query = """
    UPDATE Reported_Items
    SET is_alloted = 1
    WHERE Id = %s
    """

    datalink_cursor.execute(set_query, (Id,))

    #Move item to List_Of_Found_Items
    insert_query = """
    INSERT INTO List_Of_Found_Items
    (Id, Date, Time, Date_Returned, Time_Returned)
    SELECT Id, Date, Time, CURDATE(), CURTIME()
    FROM Reported_Items
    WHERE Id = %s AND is_alloted = 1
    """

    datalink_cursor.execute(insert_query, (Id,))

    #Remove item from Reported_Items
    delete_query = """
    DELETE FROM Reported_Items
    WHERE Id = %s AND is_alloted = 1
    """

    datalink_cursor.execute(delete_query, (Id,))

    Datalink.commit()
    Datalink.disconnect_datalink()

    button.config(text="✓ Found", state=HUD.DISABLED)


def create_report_image(obj, width=450, height=250):

    try:
        if os.path.exists(obj.picture_path):
            image = Image.open(obj.picture_path).convert("RGB")
        else:
            image = Image.new("RGB", (width, height), "black")
    except Exception:
        image = Image.new("RGB", (width, height), "black")

    image_ratio = image.width / image.height
    card_ratio = width / height

    if image_ratio > card_ratio:
        new_height = height
        new_width = int(new_height * image_ratio)
    else:
        new_width = width
        new_height = int(new_width / image_ratio)

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - width) // 2
    top = (new_height - height) // 2
    image = image.crop((left, top, left + width, top + height))

    panel_height = 105
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    overlay_draw.rectangle(
        (0, height - panel_height, width, height),
        fill=(0, 0, 0, 150)
    )

    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(image)

    report_text = (
        f"ID: {obj.id}\n"
        f"Date: {obj.date}\n"
        f"Time: {obj.time}\n"
        f"Area: {obj.area}\n"
        f"Tags: {obj.tags}"
    )

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/OCRAEXT.TTF", 12)
    except Exception:
        font = ImageFont.load_default()

    draw.multiline_text(
        (18, height - panel_height + 12),
        report_text,
        font=font,
        fill="white",
        spacing=4
    )

    return image


def search_result(home_page, search_result_page, screen, search_item):

    home_page.grid_remove()

    for widget in search_result_page.winfo_children():
        widget.destroy()

    search_result_page.grid_configure(row=0, column=0, sticky='nsew')
    search_result_page.configure(bg='black')

    HUD.Label(
        search_result_page,
        text="Search Results",
        font=("Berlin Sans FB Demi", 25),
        bg='black',
        fg='cyan',
        anchor='n'
    ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 25))

    canvas = HUD.Canvas(search_result_page, bg='black', highlightthickness=0)
    scrollbar = HUD.Scrollbar(search_result_page, orient='vertical', command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=1, column=0, sticky='nsew')
    scrollbar.grid(row=1, column=1, sticky='ns')

    search_result_page.grid_rowconfigure(1, weight=1)
    search_result_page.grid_columnconfigure(0, weight=1)

    scrollable_frame = HUD.Frame(canvas, bg='black')
    canvas_window = canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor='nw'
    )

    #Single-column layout
    scrollable_frame.grid_columnconfigure(0, weight=1)

    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", update_scroll_region)

    def resize_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", resize_scrollable_frame)

    for no, obj in enumerate(search_item.search_result):

        row = no
        column = 0

        card = HUD.Frame(
            scrollable_frame,
            bg='black',
            bd=4,
            relief='raised',
            width=450,
            height=290
        )

        card.grid(
            row=row,
            column=column,
            padx=15,
            pady=15,
            sticky='n'
        )

        card.grid_propagate(False)

        report_image = create_report_image(
            obj,
            width=450,
            height=250
        )

        photo = ImageTk.PhotoImage(report_image)

        picture_label = HUD.Label(
            card,
            image=photo,
            bg='black',
            bd=0
        )

        picture_label.image = photo

        picture_label.place(
            x=0,
            y=0,
            width=450,
            height=250
        )

        #Match percentage
        match_percent = int(round(obj.match_percent))

        match_label = HUD.Label(
            card,
            text=f"{match_percent}% MATCH",
            bg='black',
            fg='white',
            font=("OCR A Extended", 10)
        )

        match_label.place(
            x=12,
            y=257
        )

        #Match health bar
        bar_x = 12
        bar_y = 278
        bar_width = 300
        bar_height = 8

        green_width = int(bar_width * match_percent / 100)
        red_width = bar_width - green_width

        HUD.Frame(
            card,
            bg='green',
            width=green_width,
            height=bar_height
        ).place(
            x=bar_x,
            y=bar_y
        )

        if red_width > 0:
            HUD.Frame(
                card,
                bg='red',
                width=red_width,
                height=bar_height
            ).place(
                x=bar_x + green_width,
                y=bar_y
            )

        found_button = HUD.Button(
            card,
            text="□ Found",
            bg='grey',
            fg='white',
            font=("OCR A Extended", 8)
        )

        found_button.config(
            command=lambda button=found_button, Id=obj.id:
                found_item(button, Id)
        )

        found_button.place(
            relx=0.97,
            rely=0.94,
            anchor='se'
        )

    HUD.Button(
        search_result_page,
        text="Back",
        bg='grey',
        fg='white',
        command=lambda: go_home(search_result_page, home_page)
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=15
    )

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""