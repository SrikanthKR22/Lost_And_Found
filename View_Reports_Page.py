'''#|///////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import tkinter as HUD
import Datalink
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|#

def go_home(current_page, home_page):
    current_page.grid_remove()
    home_page.grid(row=0,column=0)

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def is_matched(Id):

    datalink_cursor = Datalink.get_cursor()
    get_query = """
    SELECT is_matched
    FROM Reported_Items
    WHERE Id = %s
    """
    Id_value = (Id,)

    datalink_cursor.execute(get_query, Id_value)
    match_result = datalink_cursor.fetchone()[0]

    set_query = """
    UPDATE Reported_Items
    SET is_matched = %s
    WHERE Id = %s;
    """
    values = (not match_result, Id)
    datalink_cursor.execute(set_query, values)

    Datalink.commit()
    Datalink.disconnect_datalink()

    return not match_result

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def toggle_matched(button, Id):
    new_status = is_matched(Id)
    if new_status:
        button.config(text="✓ Matched")
    else:
        button.config(text="□ Matched")

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def create_report_image(obj, width=450, height=250):

    # ============================================================
    # LOAD IMAGE
    # ============================================================

    try:
        if os.path.exists(obj.picture_path):
            image = Image.open(obj.picture_path).convert("RGB")
        else:
            image = Image.new("RGB", (width, height), "black")

    except Exception:
        image = Image.new("RGB", (width, height), "black")

    # ============================================================
    # FIT IMAGE TO ENTIRE CARD
    # ============================================================

    image_ratio = image.width / image.height
    card_ratio = width / height

    if image_ratio > card_ratio:
        new_height = height
        new_width = int(new_height * image_ratio)

    else:
        new_width = width
        new_height = int(new_width / image_ratio)

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # ============================================================
    # CENTER CROP
    # ============================================================

    left = (new_width - width) // 2
    top = (new_height - height) // 2
    image = image.crop((left, top, left + width, top + height))

    # ============================================================
    # SEMI-TRANSPARENT INFORMATION PANEL
    # ============================================================

    panel_height = 105
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        (0, height - panel_height, width, height),
        fill=(0, 0, 0, 150)
    )
    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(image)

    # ============================================================
    # REPORT INFORMATION
    # ============================================================

    report_text = (
        f"ID: {obj.id}\n"
        f"Date: {obj.date}\n"
        f"Time: {obj.time}\n"
        f"Area: {obj.area}\n"
        f"Tags: {obj.tags}"
    )

    # ============================================================
    # FONT
    # ============================================================

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/OCRAEXT.TTF",12)
    except Exception:
        font = ImageFont.load_default()

    # ============================================================
    # BURN TEXT ONTO IMAGE
    # ============================================================

    draw.multiline_text(
        (18, height - panel_height + 12),
        report_text,
        font=font,
        fill="white",
        spacing=4
    )
    return image

#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

def view_reports(home_page, view_reports_page, screen, your_report_objs):

    home_page.grid_remove()

    # ============================================================
    # CLEAR OLD CONTENT
    # ============================================================

    for widget in view_reports_page.winfo_children():
        widget.destroy()
    view_reports_page.grid_configure(row=0, column=0, sticky='nsew')
    view_reports_page.configure(bg='black')

    # ============================================================
    # TITLE
    # ============================================================

    HUD.Label(
        view_reports_page,
        text="View Your Reports",
        font=("Berlin Sans FB Demi", 25),
        bg='black',
        fg='cyan',
        anchor='n'
    ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 25))

    # ============================================================
    # SCROLLING AREA
    # ============================================================

    canvas = HUD.Canvas(view_reports_page, bg='black', highlightthickness=0)
    scrollbar = HUD.Scrollbar(view_reports_page, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=1, column=0, sticky='nsew')
    scrollbar.grid(row=1, column=1,sticky='ns')

    view_reports_page.grid_rowconfigure(1, weight=1)
    view_reports_page.grid_columnconfigure(0, weight=1)

    # ============================================================
    # INNER SCROLLABLE FRAME
    # ============================================================

    scrollable_frame = HUD.Frame(canvas, bg='black')
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    for column in range(3):
        scrollable_frame.grid_columnconfigure(column, weight=1)

    # ============================================================
    # UPDATE SCROLL REGION
    # ============================================================

    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", update_scroll_region)

    # ============================================================
    # MAKE INNER FRAME MATCH CANVAS WIDTH
    # ============================================================

    def resize_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", resize_scrollable_frame)

    # ============================================================
    # REPORT CARDS
    # ============================================================

    for no, obj in enumerate(your_report_objs):
        row = no // 3
        column = no % 3

        # --------------------------------------------------------
        # OUTER CARD
        # --------------------------------------------------------

        card = HUD.Frame(
            scrollable_frame,
            bg='black',
            bd=4,
            relief='raised',
            width=450,
            height=250
        )

        card.grid(row=row, column=column, padx=15, pady=15, sticky='nsew')
        card.grid_propagate(False)

        # --------------------------------------------------------
        # CREATE COMPOSITE IMAGE
        # --------------------------------------------------------

        report_image = create_report_image(obj, width=450, height=250)

        # --------------------------------------------------------
        # CONVERT PIL IMAGE → TKINTER IMAGE
        # --------------------------------------------------------

        photo = ImageTk.PhotoImage(report_image)

        # --------------------------------------------------------
        # SINGLE IMAGE LABEL
        # --------------------------------------------------------

        picture_label = HUD.Label(card, image=photo, bg='black', bd=0)
        picture_label.image = photo
        picture_label.place(x=0, y=0, width=450, height=250)

        # --------------------------------------------------------
        # MATCHED BUTTON
        # --------------------------------------------------------

        matched_button = HUD.Button(
            card,
            text="□ Matched",
            bg='grey',
            fg='white',
            font=("OCR A Extended", 8)
        )

        matched_button.config(
            command=lambda button=matched_button, Id=obj.id:
                toggle_matched(button,Id)
        )

        # --------------------------------------------------------
        # PLACE BUTTON AT SOUTH-EAST
        # --------------------------------------------------------

        matched_button.place(relx=0.97, rely=0.94, anchor='se')

    # ============================================================
    # BACK BUTTON
    # ============================================================

    HUD.Button(
        view_reports_page,
        text="Back",
        bg='grey',
        fg='white',
        command=lambda: go_home(view_reports_page,home_page)
    ).grid(row=3, column=0, columnspan=2, pady=15)
#]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[Func-End]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::[#

"""#|///////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""