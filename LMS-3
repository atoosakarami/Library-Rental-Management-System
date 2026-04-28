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

# -- UI -------------------------------------------------------------------------

root.grid_rowconfigure(20, weight=1)

loan_title_label = Label(root, text='Book Title (Loan Report): ', bg='#d5faa7')
loan_title = Entry(root, width=30)

late_borrower_label = Label(root, text='Borrower ID / Name (optional): ', bg='#d5faa7')
late_borrower = Entry(root, width=30)

view_borrower_id_label = Label(root, text='Borrower ID: ', bg='#d5faa7')
view_borrower_id = Entry(root, width=30)

view_book_id_label = Label(root, text='Book ID (optional): ', bg='#d5faa7')
view_book_id = Entry(root, width=30)

view_book_title_label = Label(root, text='Book Title (optional): ', bg='#d5faa7')
view_book_title = Entry(root, width=30)

# Buttons
confirm_btn = Button(root, text='Submit')
cancel_btn = Button(root, text='Cancel', command=lambda: hide_all())

# -- MAIN BUTTONS --------------------------------------------------------------

main_buttons_config = [
    ('Add Borrower', lambda: show_form('add_borrower')),
    ('Check Out Book', lambda: show_form('checkout')),
    ('Add New Book', lambda: show_form('add_book')),
    ('List Copies', lambda: show_form('list_copies')),
    ('List Borrower', lambda: show_form('list_borrower')),

    # NEW REQUIREMENTS
    ('Loaned Copies by Title', lambda: show_form('loan_report')),
    ('Borrower Late Fees', lambda: show_form('late_fees')),
    ('Borrower Book View', lambda: show_form('borrower_book_view')),
]

main_buttons = []
for i, (label, cmd) in enumerate(main_buttons_config):
    btn = Button(root, text=label, command=cmd, width=30)
    btn.grid(row=i, column=0, columnspan=2, pady=5)
    main_buttons.append(btn)

# -- HELPERS -------------------------------------------------------------------

def hide_main_buttons():
    for b in main_buttons:
        b.grid_forget()

def show_main_buttons():
    for i, b in enumerate(main_buttons):
        b.grid(row=i, column=0, columnspan=2, pady=5)

def hide_all_inputs():
    widgets = [
        loan_title_label, loan_title,
        late_borrower_label, late_borrower,
        view_borrower_id_label, view_borrower_id,
        view_book_id_label, view_book_id,
        view_book_title_label, view_book_title,
        confirm_btn, cancel_btn
    ]
    for w in widgets:
        w.grid_forget()

def clear_all():
    for e in [loan_title, late_borrower, view_borrower_id, view_book_id, view_book_title]:
        e.delete(0, END)

def hide_all():
    hide_all_inputs()
    clear_all()
    show_main_buttons()

# -- FORM ROUTER ---------------------------------------------------------------

def show_form(name):
    hide_main_buttons()
    hide_all_inputs()

    if name == 'loan_report':
        loan_title_label.grid(row=0, column=0)
        loan_title.grid(row=0, column=1)

        confirm_btn.config(command=submit_loan_report)
        confirm_btn.grid(row=1, column=0)
        cancel_btn.grid(row=1, column=1)

    elif name == 'late_fees':
        late_borrower_label.grid(row=0, column=0)
        late_borrower.grid(row=0, column=1)

        confirm_btn.config(command=submit_late_fees)
        confirm_btn.grid(row=1, column=0)
        cancel_btn.grid(row=1, column=1)

    elif name == 'borrower_book_view':
        view_borrower_id_label.grid(row=0, column=0)
        view_borrower_id.grid(row=0, column=1)

        view_book_id_label.grid(row=1, column=0)
        view_book_id.grid(row=1, column=1)

        view_book_title_label.grid(row=2, column=0)
        view_book_title.grid(row=2, column=1)

        confirm_btn.config(command=submit_borrower_book_view)
        confirm_btn.grid(row=3, column=0)
        cancel_btn.grid(row=3, column=1)

def submit_loan_report():
    title = loan_title.get().strip()

    cursor.execute('''
        SELECT LB.Branch_Id, LB.Branch_Name, COUNT(BL.Book_Id)
        FROM BOOK_LOANS BL
        JOIN BOOK B ON B.Book_Id = BL.Book_Id
        JOIN LIBRARY_BRANCH LB ON LB.Branch_Id = BL.Branch_Id
        WHERE B.Title LIKE ?
        GROUP BY LB.Branch_Id, LB.Branch_Name
    ''', ('%' + title + '%',))

    rows = cursor.fetchall()
    print("Loaned Copies per Branch:")
    for r in rows:
        print(r)

    hide_all()

def submit_late_fees():
    keyword = late_borrower.get().strip()

    query = '''
        SELECT Card_No, Name,
        printf('$%.2f',
            COALESCE(SUM(
                CASE
                    WHEN julianday(COALESCE(Returned_Date, DATE('now'))) > julianday(Due_Date)
                    THEN (julianday(COALESCE(Returned_Date, DATE('now'))) - julianday(Due_Date))
                    ELSE 0
                END
            ),0)
        ) AS LateFee
        FROM BORROWER
        LEFT JOIN BOOK_LOANS USING(Card_No)
    '''

    params = []
    if keyword:
        query += " WHERE Name LIKE ? OR CAST(Card_No AS TEXT) LIKE ?"
        params = ['%' + keyword + '%', '%' + keyword + '%']

    query += " GROUP BY Card_No ORDER BY LateFee DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    print("Borrower Late Fees:")
    for r in rows:
        print(r)

    hide_all()

def submit_borrower_book_view():
    bid = view_borrower_id.get().strip()
    book_id_val = view_book_id.get().strip()
    title = view_book_title.get().strip()

    if not bid:
        print("Borrower ID required")
        return

    query = '''
        SELECT B.Book_Id, B.Title,
        CASE
            WHEN julianday(COALESCE(BL.Returned_Date, DATE('now'))) > julianday(BL.Due_Date)
            THEN printf('$%.2f',
                (julianday(COALESCE(BL.Returned_Date, DATE('now'))) - julianday(BL.Due_Date)))
            ELSE 'Non-Applicable'
        END AS LateFee
        FROM BOOK_LOANS BL
        JOIN BOOK B ON B.Book_Id = BL.Book_Id
        WHERE BL.Card_No = ?
    '''

    params = [bid]

    if book_id_val:
        query += " AND B.Book_Id = ?"
        params.append(book_id_val)

    if title:
        query += " AND B.Title LIKE ?"
        params.append('%' + title + '%')

    query += " ORDER BY LateFee DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    print("Borrower Book View:")
    for r in rows:
        print(r)

    hide_all()

root.mainloop()
