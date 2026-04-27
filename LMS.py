# -- PyQt5: pip3 install PyQt5

# -- Tkinter: pip3 install tkinter

# -- Kivy: pip3 install kivy

from tkinter import *
import sqlite3

root = Tk()
root.title('Library Management System')
root.geometry("400x400")
root.config(bg="#d5faa7")

db = sqlite3.connect('LMS.db')
cursor = db.cursor()

# ── Hidden input widgets ──────────────────────────────────────────

# Add Borrower fields
f_name_label = Label(root, text='First Name: ', bg="#d5faa7")
f_name = Entry(root, width=30)
l_name_label = Label(root, text='Last Name: ', bg="#d5faa7")
l_name = Entry(root, width=30)

# Check Out Book fields
book_id_label = Label(root, text='Book ID: ', bg="#d5faa7")
book_id = Entry(root, width=30)
borrower_id_label = Label(root, text='Borrower ID: ', bg="#d5faa7")
borrower_id = Entry(root, width=30)

# Add New Book fields
book_title_label = Label(root, text='Book Title: ', bg="#d5faa7")
book_title = Entry(root, width=30)
book_author_label = Label(root, text='Author: ', bg="#d5faa7")
book_author = Entry(root, width=30)

# List Copies fields
copies_book_id_label = Label(root, text='Book ID: ', bg="#d5faa7")
copies_book_id = Entry(root, width=30)

# List Borrower fields
list_borrower_id_label = Label(root, text='Borrower ID: ', bg="#d5faa7")
list_borrower_id = Entry(root, width=30)

# Shared confirm/cancel buttons (hidden at start)
confirm_btn = Button(root, text="Submit")
cancel_btn = Button(root, text="Cancel", command=lambda: hide_all())

# ── All main buttons ──────────────────────────────────────────────

main_buttons_config = [
    ("Add Borrower",   lambda: show_form("add_borrower")),
    ("Check Out Book", lambda: show_form("checkout")),
    ("Add New Book",   lambda: show_form("add_book")),
    ("List Copies",    lambda: show_form("list_copies")),
    ("List Borrower",  lambda: show_form("list_borrower")),
]

main_buttons = []
for i, (label, cmd) in enumerate(main_buttons_config):
    btn = Button(root, text=label, command=cmd, width=30)
    btn.grid(row=i, column=0, columnspan=2, pady=5, padx=10)
    main_buttons.append(btn)

# ── Helper functions ──────────────────────────────────────────────

def hide_main_buttons():
    for btn in main_buttons:
        btn.grid_forget()

def show_main_buttons():
    for i, btn in enumerate(main_buttons):
        btn.grid(row=i, column=0, columnspan=2, pady=5, padx=10)

def hide_all_inputs():
    """Hide every input widget."""
    all_inputs = [
        f_name_label, f_name, l_name_label, l_name,
        book_id_label, book_id, borrower_id_label, borrower_id,
        book_title_label, book_title, book_author_label, book_author,
        copies_book_id_label, copies_book_id,
        list_borrower_id_label, list_borrower_id,
        confirm_btn, cancel_btn,
    ]
    for w in all_inputs:
        w.grid_forget()

def clear_all_entries():
    for entry in [f_name, l_name, book_id, borrower_id,
                  book_title, book_author, copies_book_id, list_borrower_id]:
        entry.delete(0, END)

def hide_all():
    """Cancel — go back to main menu."""
    hide_all_inputs()
    clear_all_entries()
    show_main_buttons()

# ── Show form based on which button was clicked ───────────────────

def show_form(form_name):
    hide_main_buttons()
    hide_all_inputs()

    forms = {
        "add_borrower": [
            (f_name_label, 0, 0), (f_name, 0, 1),
            (l_name_label, 1, 0), (l_name, 1, 1),
        ],
        "checkout": [
            (book_id_label, 0, 0),     (book_id, 0, 1),
            (borrower_id_label, 1, 0), (borrower_id, 1, 1),
        ],
        "add_book": [
            (book_title_label, 0, 0),  (book_title, 0, 1),
            (book_author_label, 1, 0), (book_author, 1, 1),
        ],
        "list_copies": [
            (copies_book_id_label, 0, 0), (copies_book_id, 0, 1),
        ],
        "list_borrower": [
            (list_borrower_id_label, 0, 0), (list_borrower_id, 0, 1),
        ],
    }

    # Grid the correct input widgets
    for widget, row, col in forms[form_name]:
        widget.grid(row=row, column=col, padx=10, pady=5)

    # Map form to its submit function
    submit_commands = {
        "add_borrower":  submit_borrower,
        "checkout":      submit_checkout,
        "add_book":      submit_book,
        "list_copies":   submit_list_copies,
        "list_borrower": submit_list_borrower,
    }

    next_row = len(forms[form_name]) // 2  # one row per label+entry pair
    confirm_btn.config(command=submit_commands[form_name])
    confirm_btn.grid(row=next_row, column=0, pady=10, padx=10, ipadx=60)
    cancel_btn.grid(row=next_row, column=1, pady=10, padx=10, ipadx=60)

# ── Submit functions ──────────────────────────────────────────────

def submit_borrower():
    print(f"Adding borrower: {f_name.get()} {l_name.get()}")
    hide_all()

def submit_checkout():
    print(f"Checking out book ID {book_id.get()} to borrower {borrower_id.get()}")
    hide_all()

def submit_book():
    print(f"Adding book: {book_title.get()} by {book_author.get()}")
    hide_all()

def submit_list_copies():
    print(f"Listing copies for book ID: {copies_book_id.get()}")
    hide_all()

def submit_list_borrower():
    print(f"Listing borrower ID: {list_borrower_id.get()}")
    hide_all()

root.mainloop()