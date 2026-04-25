# -- PyQt5: pip3 install PyQt5

# -- Tkinter: pip3 install tkinter

# -- Kivy: pip3 install kivy

from tkinter import *

import sqlite3

#create tkinter window

root = Tk()

root.title('Address Book')

root.geometry("400x400") #x-axis y-axis place



#connect to the DB

conn = sqlite3.connect('address_book.db')
print("Connected to DB Succesfully")

#create DB cursor 
add_addressTable_c = conn.cursor()

# add_addressTable_c.execute('''CREATE TABLE ADDRESSES(FIRST_NAME TEXT,
# 					LAST_NAME TEXT,
# 					ADDRESS TEXT,
# 					CITY TEXT,
# 					STATE TEXT,
# 					ZIPCODE INT)''')


#define the submit function

def submit():
	submit_conn = sqlite3.connect('address_book.db')
	submit_cur = submit_conn.cursor()


	submit_cur.execute("INSERT INTO ADDRESSES VALUES(:f_name, :l_name, :street, :city, :state, :zcode)",
		{
			'f_name': f_name.get(),
			'l_name': l_name.get(),
			'street': street.get(),
			'city': city.get(),
			'state': state.get(),
			'zcode': zcode.get()
		})
	submit_conn.commit()
	submit_conn.close()


#based on a city and state list names 

def input_query():

	iq_conn = sqlite3.connect('address_book.db')
	iq_cur = iq_conn.cursor()

	iq_cur.execute("SELECT FIRST_NAME, LAST_NAME FROM ADDRESSES WHERE CITY = ? AND STATE = ?",
		(city.get(), state.get(),))

	records = iq_cur.fetchall()

	print(records)

	print_records = ''

	for record in records:
		print_records += str(record[0] + " " + record[1] + "\n")

	iq_label = Label(root, text = print_records)
	iq_label.grid(row = 9, column = 0, columnspan = 2)

	iq_conn.commit()
	iq_conn.close()



#define all the GUI components on the tkinter root window
# place your wdgets: place / grid / pack


#defne all textboxes
f_name = Entry(root, width = 30)
f_name.grid(row = 0, column = 1, padx = 20)

l_name = Entry(root, width = 30)
l_name.grid(row = 1, column = 1)

street = Entry(root, width = 30)
street.grid(row = 2, column = 1)

city = Entry(root, width = 30)
city.grid(row = 3, column = 1)

state = Entry(root, width = 30)
state.grid(row = 4, column = 1)

zcode = Entry(root, width = 30)
zcode.grid(row = 5, column = 1)



#define all labels
f_name_label = Label(root, text ='First Name: ')
f_name_label.grid(row = 0, column = 0)

l_name_label = Label(root, text ='Last Name: ')
l_name_label.grid(row = 1, column = 0)

st_label = Label(root, text ='Street: ')
st_label.grid(row = 2, column = 0)

city_label = Label(root, text ='City: ')
city_label.grid(row = 3, column = 0)

state_label = Label(root, text ='State: ')
state_label.grid(row = 4, column = 0, sticky = "w")

zcode_label = Label(root, text ='Zipcode: ')
zcode_label.grid(row = 5, column = 0)

#submit button -- adds a new record to the address table

submit_btn = Button(root, text = "Add Address", command = submit)
submit_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)

input_query_btn = Button(root, text= "Show Records", command = input_query)
input_query_btn.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)






root.mainloop()