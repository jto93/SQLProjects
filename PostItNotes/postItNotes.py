#Post It Notes Program using Tkinter and SQL DB
# Following from source: https://www.studytonight.com/python-projects/post-it-notes-application-python-project
# Purpose of this is to use a GUI combined with Database 

from email import message
import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry



def createTable(): 
    try: 
        cur.execute('''CREATE TABLE notes_table
                        (date text, notes_title text, notes text)''')

    except: 
        print('Table already exists')

#Insert a row of data into the database
def add_notes():
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0", "end-1c")

    if (len(today) <=0) & (len(notes_title)<=0) & (len(notes)<=1): 
        messagebox.showerror(message = "Enter Required Details")
    
    else: 
        with connection: 
            #insert into the table
            sql_statement = "INSERT INTO notes_table VALUES ('%s','%s','%s')" %(today,notes_title,notes)
            cur.execute(sql_statement)
            messagebox.showinfo(message="Note added")

#View all notes
def view_notes():
    #obtain user input
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    #If no input given, retrieve all notes
    if (len(date) <=0) & (len(notes_title)<=0):
        sql_statement = "SELECT * FROM notes_table"
    
    #Retrieve Notes Matching a title
    elif (len(date) <= 0) & (len(notes_title)>0):
        sql_statement = "SELECT * FROM notes_table where notes_title='%s'"%(notes_title)

    #Retrieve Notes Matching a Date
    elif (len(date) > 0) & (len(notes_title)<=0):
        sql_statement = "SELECT * FROM notes_table where date ='%s'" %(date)
    #Retrieve Notes Matching date and Title
    else:
        sql_statement = "SELECT * FROM notes_table where date ='%s' and notes_title='%s'" %(date,notes_title)

    #Execute the query
    cur.execute(sql_statement)

    #Obtain query contents
    row = cur.fetchall()
    #Check if no contents were received
    if len(row)<=0:
        messagebox.showerror(message="No note found")
    else: 
        for i in row: 
            messagebox.showinfo(message="Date: "+i[0]+"\nTitle: "+i[1]+"\nNotes: "+i[2])

#Delete a note or notes
def delete_notes():

    with connection: 

        #obtain input
        date = date_entry.get()
        notes_title = notes_title_entry.get()
        #Ask if user wants to delete all of their notes
        choice = messagebox.askquestion(message="Do you want to delete all notes?")
        #If yes, delete all
        choice = choice.lower()

        if choice == 'yes':
            sql_statement = "DELETE FROM notes_table"

        #Delete notes matching a particular date and title
        else: 
            if (len(date) <= 0 ) & (len(notes_title)<=0): 
                
                #raise error if no input
                messagebox.showerror(message="Please enter required details")

            else: 
                sql_statement = "DELETE FROM notes_table WHERE date='%s' and notes_title='%s'" %(date, notes_title)

        #Execute the query
        cur.execute(sql_statement)

        messagebox.showinfo(message="Note(s) Deleted")


#Update a note or notes
def update_notes():
    with connection:
        #Obtain user input
        date = date_entry.get()
        notes_title = notes_title_entry.get()
        notes = notes_entry.get("1.0", "end-1c")
        #Check if input is given by user
        if (len(date) <=0) & (len(notes_title)<=0) & (len(notes)<=1):
            messagebox.showerror(message="Please enter required details")
        #udpate news
        else: 
            sql_statement = "UPDATE notes_table SET notes = '%s' WHERE date = '%s' and notes_title = '%s'" %(notes, date, notes_title)

        #Execute the query
        cur.execute(sql_statement)
        messagebox.showinfo(message="Note updated")



global connection, cur, sql_statement
#Hook up with SQL Table
connection = sql.connect(':memory:')
cur = connection.cursor()

createTable()

#View a window in Tkinter
window = Tk()
#Set Window Size
window.geometry("500x300")
window.title('Post It Note')
title_label = Label(window, text='Post It Note').pack()

#Read in input
date_label = Label(window, text="Date: ").place(x=10, y=20)
date_entry = DateEntry(window, width=20)
date_entry.place(x=50,y=20)

#Notes Title
notes_title_label = Label(window, text="Notes title:").place(x=10,y=50)
notes_title_entry = Entry(window, width=30)
notes_title_entry.place(x=80,y=50)

#Notes
notes_label = Label(window, text="Notes: ").place(x=10, y=90)
notes_entry = Text(window, width=50,height=10)
notes_entry.place(x=60,y=90)

#Perform Notes Functions
button1 = Button(window, text="Add Note", bg = 'Grey', fg='Black', command=add_notes).place(x=10,y=260)
button2 = Button(window, text="View Note", bg = 'Grey', fg='Black', command=view_notes).place(x=110,y=260)
button3 = Button(window, text="Delete Note", bg = 'Grey', fg='Black', command=delete_notes).place(x=210,y=260)
button4 = Button(window, text="Update Note", bg = 'Grey', fg='Black', command=update_notes).place(x=310,y=260)

window.mainloop()
connection.close()

    



