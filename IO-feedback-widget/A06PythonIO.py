#!/usr/bin/python3
# feedback form by John Swanson
# IST 402 M06: Python IO Lab

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import sqlite3


class FeedbackIO:

    def __init__(self, master):
        # master root window
        master.title('IST 402 Feedback Form JCS6270')
        master.resizable(False, False)
    

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 14))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        # Dropdown Menu Frame
        self.frame_menu = ttk.Frame(master)
        self.frame_menu.grid(column=0, row=0, sticky=(N, W, E, S))
        self.frame_menu.columnconfigure(0, weight=1)
        self.frame_menu.rowconfigure(0, weight=1)
        self.frame_menu.pack(expand=150, ipadx=50)

        # Dropdown contents -States
        locations = ['California', 'Seattle', 'Oregon', 'New York', 'Florida']
        self.curr_location = StringVar()
        self.curr_location.set(locations[0])
        self.dropdown_menu = ttk.OptionMenu(self.frame_menu, self.curr_location, *locations).grid(row=0, column=1,
                                            ipady=10, padx=30,sticky='se')
        ttk.Label(self.frame_menu, style='TLabel', text="What state did you visit? ").grid(row=0, column=0, ipady=20,
                                            sticky='n')

        # Radiobutton  age-range
        ttk.Label(self.frame_menu, style='TLabel', text="What is your age range?").grid(row=2, column=0, ipady=10,
                                                                                                        sticky='s')
        self.radiobutton = StringVar()
        
        ttk.Radiobutton(self.frame_menu, text='18-29',variable=self.radiobutton, value='18-29').grid(row=3, column=0,
                                                                                                ipadx=25, sticky='e')
        ttk.Radiobutton(self.frame_menu, text='30-45', variable=self.radiobutton, value='30-45').grid(row=3, column=1,
                                                                                                         sticky='w')
        ttk.Radiobutton(self.frame_menu, text='45-55',variable=self.radiobutton, value='45-55').grid(row=4, column=0,
                                                                                                ipadx=25, sticky='e')
        ttk.Radiobutton(self.frame_menu, text='55+',variable=self.radiobutton, value='55+').grid(row=4, column=1,
                                                                                                         sticky='w')
        ttk.Label(self.frame_menu, text="Did you travel alone? ").grid(row=5, column=0, ipady=10, sticky='s')
        
        self.checkbox_yes = StringVar()
        self.checkbox_no = StringVar()
        
        ttk.Checkbutton(self.frame_menu, variable=self.checkbox_yes, text='Yes').grid(row=6, column=0,ipadx=15,sticky='e')                                                                                                  
        ttk.Checkbutton(self.frame_menu, variable=self.checkbox_no, text='No').grid(row=6, column=1,sticky='w')
                                                                                                        

        # Header Frame
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        # Header contents
        ttk.Label(self.frame_header, text='Thanks for Traveling With Us!', style='Header.TLabel').grid(row=0, column=1)
        ttk.Label(self.frame_header, wraplength=300,
                  text=("We're glad you chose Explore America for your recent adventure.  "
                        "Please tell us what you thought about your tour.")).grid(row=1, column=1)

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, style='TLabel', text='Name:').grid(row=0, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, style='TLabel', text='Email:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, style='TLabel', text='Comments:').grid(row=2, column=0, padx=5, sticky='sw')

        self.entry_name = ttk.Entry(self.frame_content, width=24, font=('Arial', 11))
        self.entry_email = ttk.Entry(self.frame_content, width=24, font=('Arial', 11))
        self.text_comments = Text(self.frame_content, width=50, height=10, font=('Arial', 11))

        self.entry_name.grid(row=1, column=0, padx=5)
        self.entry_email.grid(row=1, column=1, padx=5)
        self.text_comments.grid(row=3, column=0, columnspan=2, padx=5)

        ttk.Button(self.frame_content, text='Print to Console',
                   command=self.submit).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        ttk.Button(self.frame_content, text='Flat File',
                   command=self.file_write).grid(row=4, column=1, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='JSON File',
                   command=self.jsonfile_write).grid(row=5, column=0, padx=5, pady=5, sticky='w')
        ttk.Button(self.frame_content, text='SQL File',
                   command=self.sqlfile_write).grid(row=5, column=1, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear',
                   command=self.clear).grid(row=6, column=0, padx=5, pady=5, sticky='w')

    def jsonfile_write(self):
        #Creating a Survey Object
        jsonfile = Survey()
        jsonfile.state = self.curr_location.get()
        jsonfile.age_range = self.radiobutton.get()
        
        # Checking Boolean
        if self.checkbox_yes.get() == '1':
            jsonfile.trav_alone = 'Travelling Alone? : Yes'
        elif self.checkbox_no.get() == '1':
            jsonfile.trav_alone = 'Travelling Alone? : No'
        else:
            jsonfile.trav_alone = 'Travelling Alone? : Unknown'
            
        jsonfile.name = self.entry_name.get()
        jsonfile.email = self.entry_email.get()
        jsonfile.comments = self.text_comments.get(1.0, 'end')

        with open('survey.json', 'w') as i:
            i.write(json.dumps(jsonfile.__dict__))

            
        print(json.dumps(jsonfile.__dict__))
        messagebox.showinfo(title='Explore {}'.format(jsonfile.state) + ' FeedbackWidget',
                            message='Your {}'.format(jsonfile.state) + ' survey.json File Submitted!')

    def file_write(self):
        output = open('survey.txt', 'w')
        output.write('Visited State: {}'.format(self.curr_location.get()) + '\n')
        output.write('Age Range: {}'.format(self.radiobutton.get()) + '\n')
        
        # Checking Boolean       
        if self.checkbox_yes.get() == '1':
            trav_alone = 'Travelling Alone: Yes \n'
        elif self.checkbox_no.get() == '1':
            trav_alone = 'Travelling Alone: No \n'
        else:
            trav_alone = 'Travelling Alone: Unknown \n'
            
        output.write(trav_alone)
        output.write('Name: {}'.format(self.entry_name.get()))
        output.write('Email: {}'.format(self.entry_email.get()))
        output.write('Comments: {}'.format(self.text_comments.get(1.0, 'end')))
        output.close()
        print('File Write Complete')
        messagebox.showinfo(title='Explore {}'.format(self.curr_location.get()) + ' FeedbackWidget',
                            message='Your {}'.format(self.curr_location.get()) + ' Survey Saved In survey.txt !')

    def sqlfile_write(self):
        survey = 'survey'
        state = self.curr_location.get() + ' '
        age_range = self.radiobutton.get() + ' '
        
        # Checking Boolean        
        if self.checkbox_yes.get() == '1':
            trav_alone = 'Travelling Alone: Yes \n'
        elif self.checkbox_no.get() == '1':
            trav_alone = 'Travelling Alone: No \n'
        else:
            trav_alone = 'Travelling Alone: Unknown \n'
            
        name = self.entry_name.get() + ' '
        email = self.entry_email.get() + ' '
        comments = self.text_comments.get(1.0, 'end')
        #:memory:
        db_file = 'db_survey.db'
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute('DROP TABLE if exists survey')
        cur.execute('CREATE TABLE {tn} ({nf} {ft})'
                    .format(tn=survey, nf='state', ft='TEXT'))
        cur.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                    .format(tn=survey, cn='age_range', ct='TEXT'))
        cur.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                    .format(tn=survey, cn='trav_alone', ct='TEXT'))
        cur.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                    .format(tn=survey, cn='name', ct='TEXT'))
        cur.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                    .format(tn=survey, cn='email', ct='TEXT'))
        cur.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                    .format(tn=survey, cn='comments', ct='TEXT'))

        cur.execute("INSERT into survey (state, age_range, trav_alone, name, email, comments) values (?, ?, ?, ?, ?, ?)",
                    (state, age_range, trav_alone, name, email, comments))

        #Displaying the Database Row Selection in Console
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM survey')
        r = cur.fetchone()
        print(type(r))
        con.commit()
        for row in r:
            print(row)
        cur.close()
        con.close()

        messagebox.showinfo(title='Explore {}'.format(self.curr_location) + ' FeedbackWidget',
                            message='Your {}'.format(self.curr_location) + ' db_survey.db Survey File Submitted!')

    def submit(self):
        print('Visited State: {}'.format(self.curr_location.get()))
        print('Age Range: {}'.format(self.radiobutton.get()))

        # Checking boolean with if/else conditions
        if self.checkbox_yes.get() == '1':
            print('Travelling Alone? : Yes \n')
        elif self.checkbox_no.get() == '1':
            print('Travelling Alone? : No \n')
        else:
            print('Travelling Alone? : Unknown \n')

        print('Name: {}'.format(self.entry_name.get()))
        print('Email: {}'.format(self.entry_email.get()))
        print('Comments: {}'.format(self.text_comments.get(1.0, 'end')))

        messagebox.showinfo(title='Explore {}'.format(self.curr_location.get()) + ' FeedbackWidget',
                            message='Your {}'.format(self.curr_location.get()) + ' Comments Submitted!')
       

    def clear(self):
        self.curr_location.set('California')
        self.radiobutton.set(NONE)
        self.checkbox_yes.set(NONE)
        self.checkbox_no.set(NONE)
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.text_comments.delete(1.0, 'end')


class Survey:
    location = ' '
    age_range = ' '
    trav_alone = ' '
    name = ' '
    email = ' '
    comments = ' '


def main():
    root = Tk()
    feedbackIO = FeedbackIO(root)
    root.mainloop()


if __name__ == "__main__": main()
