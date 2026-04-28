from tkinter import *
 import sqlite3
root = Tk()
 root.title('Library Management System')
 root.geometry('400x400')
 root.config(bg='#d5faa7')
db = sqlite3.connect('LMS.db')
 cursor = db.cursor()
 cursor.execute('PRAGMA foreign_keys = ON;')
# -- Initialize database tables -------------------------------------------------
cursor.execute('''
 CREATE TABLE IF NOT EXISTS PUBLISHER (
     Publisher_Name VARCHAR(50) NOT NULL,
     Phone VARCHAR(20),
     Address VARCHAR(100),
     PRIMARY KEY (Publisher_Name)
 )
 ''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS LIBRARY_BRANCH (
     Branch_Id INTEGER PRIMARY KEY AUTOINCREMENT,
     Branch_Name VARCHAR(50) NOT NULL,
     Branch_Address VARCHAR(100),
     UNIQUE (Branch_Name)
 )
 ''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS BORROWER (
     Card_No INTEGER PRIMARY KEY AUTOINCREMENT,
     Name VARCHAR(50) NOT NULL,
     Address VARCHAR(100),
     Phone VARCHAR(20)
 )
 ''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS BOOK (
     Book_Id INTEGER PRIMARY KEY AUTOINCREMENT,
     Title VARCHAR(100) NOT NULL,
     Publisher_Name VARCHAR(50) NOT NULL,
     FOREIGN KEY (Publisher_Name) REFERENCES PUBLISHER (Publisher_Name)
         ON UPDATE CASCADE
         ON DELETE RESTRICT
 )
 ''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS BOOK_LOANS (
     Book_Id INT NOT NULL,
     Branch_Id INT NOT NULL,
     Card_No INT NOT NULL,
     Date_Out DATE NOT NULL,
     Due_Date DATE NOT NULL,
     Returned_Date DATE,
     PRIMARY KEY (Book_Id, Branch_Id, Card_No, Date_Out),
     FOREIGN KEY (Book_Id) REFERENCES BOOK (Book_Id)
         ON UPDATE CASCADE
         ON DELETE RESTRICT,
     FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH (Branch_Id)
         ON UPDATE CASCADE
         ON DELETE RESTRICT,
     FOREIGN KEY (Card_No) REFERENCES BORROWER (Card_No)
         ON UPDATE CASCADE
         ON DELETE RESTRICT,
     CHECK (Due_Date >= Date_Out)
 )
 ''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS BOOK_COPIES (
     Book_Id INT NOT NULL,
     Branch_Id INT NOT NULL,
     No_Of_Copies INT NOT NULL,
     PRIMARY KEY (Book_Id, Branch_Id),
     FOREIGN KEY (Book_Id) REFERENCES BOOK (Book_Id)
         ON UPDATE CASCADE
         ON DELETE RESTRICT,
     FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH (Branch_Id)
         ON UPDATE CASCADE
         ON DELETE RESTRICT
 )
 ''')
cursor.execute('''
 CREATE TABLE IF NOT EXISTS BOOK_AUTHORS (
     Book_Id INT NOT NULL,
     Author_Name VARCHAR(50) NOT NULL,
     PRIMARY KEY (Book_Id, Author_Name),
     FOREIGN KEY (Book_Id) REFERENCES BOOK (Book_Id)
         ON UPDATE CASCADE
         ON DELETE RESTRICT
 )
 ''')
cursor.execute('''
 CREATE TRIGGER IF NOT EXISTS update_copies_after_checkout
 AFTER INSERT ON BOOK_LOANS
 BEGIN
     UPDATE BOOK_COPIES
     SET No_Of_Copies = No_Of_Copies - 1
     WHERE Book_Id = NEW.Book_Id
       AND Branch_Id = NEW.Branch_Id;
 END;
 ''')
db.commit()
# -- Helper records -------------------------------------------------------------
def ensure_default_branch():
     cursor.execute('''
         INSERT OR IGNORE INTO LIBRARY_BRANCH (Branch_Id, Branch_Name, Branch_Address)
         VALUES (1, 'Main Branch', 'Default Address')
     ''')
def ensure_default_publisher():
     cursor.execute('''
         INSERT OR IGNORE INTO PUBLISHER (Publisher_Name)
         VALUES ('DefaultPublisher')
     ''')
def ensure_five_branches():
     branch_seed = [
         (1, 'Main Branch', 'Default Address 1'),
         (2, 'West Branch', 'Default Address 2'),
         (3, 'East Branch', 'Default Address 3'),
         (4, 'North Branch', 'Default Address 4'),
         (5, 'South Branch', 'Default Address 5'),
     ]
     cursor.executemany('''
         INSERT OR IGNORE INTO LIBRARY_BRANCH (Branch_Id, Branch_Name, Branch_Address)
         VALUES (?, ?, ?)
     ''', branch_seed)
# -- Hidden input widgets -------------------------------------------------------
# Add Borrower fields
 borrower_name_label = Label(root, text='Borrower Name: ', bg='#d5faa7')
 borrower_name = Entry(root, width=30)
 address_label = Label(root, text='Address: ', bg='#d5faa7')
 address = Entry(root, width=30)
 phone_label = Label(root, text='Phone: ', bg='#d5faa7')
 phone = Entry(root, width=30)
# Check Out Book fields
 book_id_label = Label(root, text='Book ID: ', bg='#d5faa7')
 book_id = Entry(root, width=30)
 borrower_id_label = Label(root, text='Borrower ID: ', bg='#d5faa7')
 borrower_id = Entry(root, width=30)
# Add New Book fields
 book_title_label = Label(root, text='Book Title: ', bg='#d5faa7')
 book_title = Entry(root, width=30)
 book_publisher_label = Label(root, text='Publisher: ', bg='#d5faa7')
 book_publisher = Entry(root, width=30)
 book_author_label = Label(root, text='Author: ', bg='#d5faa7')
 book_author = Entry(root, width=30)
# List Copies fields
 copies_book_id_label = Label(root, text='Book ID: ', bg='#d5faa7')
 copies_book_id = Entry(root, width=30)
# List Borrower fields
 list_borrower_id_label = Label(root, text='Borrower ID: ', bg='#d5faa7')
 list_borrower_id = Entry(root, width=30)
# Shared confirm/cancel buttons (hidden at start)
 confirm_btn = Button(root, text='Submit')
 cancel_btn = Button(root, text='Cancel', command=lambda: hide_all())
# -- Main buttons ---------------------------------------------------------------
main_buttons_config = [
     ('Add Borrower', lambda: show_form('add_borrower')),
     ('Check Out Book', lambda: show_form('checkout')),
     ('Add New Book', lambda: show_form('add_book')),
     ('List Copies', lambda: show_form('list_copies')),
     ('List Borrower', lambda: show_form('list_borrower')),
 ]
main_buttons = []
 for i, (label, cmd) in enumerate(main_buttons_config):
     btn = Button(root, text=label, command=cmd, width=30)
     btn.grid(row=i, column=0, columnspan=2, pady=5, padx=10)
     main_buttons.append(btn)
# -- UI helpers ----------------------------------------------------------------
def hide_main_buttons():
     for btn in main_buttons:
         btn.grid_forget()
def show_main_buttons():
     for i, btn in enumerate(main_buttons):
         btn.grid(row=i, column=0, columnspan=2, pady=5, padx=10)
def hide_all_inputs():
     all_inputs = [
         borrower_name_label, borrower_name, address_label, address, phone_label, phone,
         book_id_label, book_id, borrower_id_label, borrower_id,
         book_title_label, book_title, book_publisher_label, book_publisher,
         book_author_label, book_author,
         copies_book_id_label, copies_book_id,
         list_borrower_id_label, list_borrower_id,
         confirm_btn, cancel_btn,
     ]
     for widget in all_inputs:
         widget.grid_forget()
def clear_all_entries():
     for entry in [
         borrower_name, address, phone,
         book_id, borrower_id,
         book_title, book_publisher, book_author,
         copies_book_id, list_borrower_id,
     ]:
         entry.delete(0, END)
def hide_all():
     hide_all_inputs()
     clear_all_entries()
     show_main_buttons()
# -- Form routing ---------------------------------------------------------------
def show_form(form_name):
     hide_main_buttons()
     hide_all_inputs()
    forms = {
         'add_borrower': [
             (borrower_name_label, 0, 0), (borrower_name, 0, 1),
             (address_label, 1, 0), (address, 1, 1),
             (phone_label, 2, 0), (phone, 2, 1),
         ],
         'checkout': [
             (book_id_label, 0, 0), (book_id, 0, 1),
             (borrower_id_label, 1, 0), (borrower_id, 1, 1),
         ],
         'add_book': [
             (book_title_label, 0, 0), (book_title, 0, 1),
             (book_publisher_label, 1, 0), (book_publisher, 1, 1),
             (book_author_label, 2, 0), (book_author, 2, 1),
         ],
         'list_copies': [
             (copies_book_id_label, 0, 0), (copies_book_id, 0, 1),
         ],
         'list_borrower': [
             (list_borrower_id_label, 0, 0), (list_borrower_id, 0, 1),
         ],
     }
    for widget, row, col in forms[form_name]:
         widget.grid(row=row, column=col, padx=10, pady=5)
    submit_commands = {
         'add_borrower': submit_borrower,
         'checkout': submit_checkout,
         'add_book': submit_book,
         'list_copies': submit_list_copies,
         'list_borrower': submit_list_borrower,
     }
    next_row = len(forms[form_name]) // 2
     confirm_btn.config(command=submit_commands[form_name])
     confirm_btn.grid(row=next_row, column=0, pady=10, padx=10, ipadx=60)
     cancel_btn.grid(row=next_row, column=1, pady=10, padx=10, ipadx=60)
# -- Submit handlers ------------------------------------------------------------
def submit_borrower():
     name = borrower_name.get().strip()
     addr = address.get().strip()
     phone_num = phone.get().strip()
    if not name or not addr or not phone_num:
         print('Error: Required fields missing')
         return
    try:
         cursor.execute('''
             INSERT INTO BORROWER (Name, Address, Phone)
             VALUES (?, ?, ?)
         ''', (name, addr, phone_num))
         new_card_no = cursor.lastrowid
         db.commit()
         print(f'Borrower added: {name}')
         print(f'New card number: {new_card_no}')
     except sqlite3.Error as e:
         print(f'Database error: {e}')
    hide_all()
def submit_checkout():
     selected_book_id = book_id.get().strip()
     selected_borrower_id = borrower_id.get().strip()
    if not selected_book_id or not selected_borrower_id:
         print('Error: Book ID and Borrower ID are required')
         return
    try:
         ensure_default_branch()
         cursor.execute('''
             INSERT INTO BOOK_LOANS
             (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date, Returned_Date)
             VALUES (?, ?, ?, DATE('now'), DATE('now', '+7 days'), NULL)
         ''', (selected_book_id, 1, selected_borrower_id))
         db.commit()
        cursor.execute('''
             SELECT Book_Id, Branch_Id, No_Of_Copies
             FROM BOOK_COPIES
             WHERE Book_Id = ?
         ''', (selected_book_id,))
        rows = cursor.fetchall()
         print('Checkout successful.')
         if rows:
             print('Updated copies:')
             for row in rows:
                 print(row)
         else:
             print('No copy record found for this book in branch 1.')
    except sqlite3.Error as e:
         print(f'Database error: {e}')
    hide_all()
def submit_book():
     title = book_title.get().strip()
     publisher = book_publisher.get().strip()
     author = book_author.get().strip()
    if not title or not publisher or not author:
         print('Error: Book title, publisher, and author are required')
         return
    try:
         ensure_five_branches()
        cursor.execute('''
             SELECT 1
             FROM PUBLISHER
             WHERE Publisher_Name = ?
         ''', (publisher,))
         publisher_exists = cursor.fetchone()
        if not publisher_exists:
             print('Error: Publisher does not exist. Use an existing publisher name.')
             return
        cursor.execute('''
             INSERT INTO BOOK (Title, Publisher_Name)
             VALUES (?, ?)
         ''', (title, publisher))
         new_book_id = cursor.lastrowid
        cursor.execute('''
             INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name)
             VALUES (?, ?)
         ''', (new_book_id, author))
        copies_seed = [(new_book_id, branch_id, 5) for branch_id in range(1, 6)]
         cursor.executemany('''
             INSERT OR REPLACE INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies)
             VALUES (?, ?, ?)
         ''', copies_seed)
        db.commit()
         print(f'Book added: {title} (Book ID: {new_book_id})')
         print(f'Publisher: {publisher}')
         print('Inserted 5 copies into branches 1-5.')
    except sqlite3.Error as e:
         print(f'Database error: {e}')
    hide_all()
def submit_list_copies():
     selected_book_id = copies_book_id.get().strip()
    if not selected_book_id:
         print('Error: Book ID is required')
         return
    try:
         cursor.execute('''
             SELECT Book_Id, Branch_Id, No_Of_Copies
             FROM BOOK_COPIES
             WHERE Book_Id = ?
         ''', (selected_book_id,))
        rows = cursor.fetchall()
         print('Copies:')
         if rows:
             for row in rows:
                 print(row)
         else:
             print('No copy records found.')
    except sqlite3.Error as e:
         print(f'Database error: {e}')
    hide_all()
def submit_list_borrower():
     selected_borrower_id = list_borrower_id.get().strip()
    if not selected_borrower_id:
         print('Error: Borrower ID is required')
         return
    try:
         cursor.execute('''
             SELECT Card_No, Name, Address, Phone
             FROM BORROWER
             WHERE Card_No = ?
         ''', (selected_borrower_id,))
        rows = cursor.fetchall()
         print('Borrower:')
         if rows:
             for row in rows:
                 print(row)
         else:
             print('No borrower found with that ID.')
    except sqlite3.Error as e:
         print(f'Database error: {e}')
    hide_all()
root.mainloop()
