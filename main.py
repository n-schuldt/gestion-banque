from tkinter import *
import os
import random
# main screen
master = Tk()
master.title('Banking App')
master.geometry('500x500')

# functions


def login():
    '''Login for login session'''
    path = './users'  # Need to change the path to the user file
    users_acc = os.listdir(path)
    login_name = temp_login_id.get()
    login_password = temp_login_password.get()

    for id in users_acc:
        if id == login_name:
            file = open(id, 'r')
            data = file.read()
            data = data.split('\n')
            password = data[1]

            # Dashboard
            if login_password == password:
                master.destroy
                acc_dashboard = Tk()
                acc_dashboard.title('Dashboard')
                return


# Vars
global temp_login_id
global temp_login_password
global login_notif
temp_login_id = StringVar()
temp_login_password = StringVar()  # Temporary

# Screen
Label(master, text='Identifiant', font=('Calibri', 12)).grid(
    row=1, sticky=W)  # Dont show up
Label(master, text='Password', font=('Calibri', 12)).grid(
    row=2, sticky=W)  # Dont show up
login_notif = Label(master, font=('Calibri', 12)).grid(row=4, sticky=N)

# Entry
Entry(master, textvariable=temp_login_id).grid(row=1, column=1, padx=5)
Entry(master, textvariable=temp_login_password,
      show='*'
      ).grid(row=2, column=1, padx=5)  # Temporary


# buttons for keypad
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# randomize nums list
random.shuffle(nums)
# random buttons for keypad
for i in range(10):
    print(nums[i])
    Button(master, text=nums[i], font=('Calibri', 12),
           command=lambda n=nums[i]: temp_login_password.set(temp_login_password.get() + n)).grid(row=i//3+5, column=i % 3, padx=3, pady=3)

Button(master, text='Delete', font=('Calibri', 12),
       command=lambda: temp_login_password.set(temp_login_password.get()[:-1])).grid(row=8, column=0, padx=3, pady=3)
Button(master, text='Login', font=('Calibri', 12),
       command=login).grid(row=8, column=2, padx=5, pady=5)

master.mainloop()
