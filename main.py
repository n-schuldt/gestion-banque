from tkinter import *
import os
import random
# main screen
master = Tk()
master.title('Banking App')
master.geometry('500x500')

# functions

def cesar(text, key=3, encrypted = True ):
    '''Str x Int --> Str
    Function to encrypt or decrypt a text'''
    if encrypted:
        text = str(text)
        encrypt = ''
        for i in text:
            ascii_lst = ord(i) + key
            encrypt += chr(ascii_lst)
        return encrypt
    else : 
        decrypt = ''
        for i in text: 
            ascii_lst = ord(i) - key
            decrypt += chr(ascii_lst)
        return decrypt

# need to add cesar function to login fuction

def login():
    '''Login for login session'''
    path = 'ident.txt'
    login_id = temp_login_id.get()
    login_password = temp_login_password.get()
    login_id = cesar(login_id)
    login_password = cesar(login_password)
    
    # cherche the id in 'ident.txt'
    file = open(path, 'r')
    data = file.readlines()
    total = len(data)
    print(data)
    print(data[0][:8])
    # loop for searching the id in the file
    for i in range(total):
        data[i] = data[i].split('*')
        print(data[i])
        line_id = data[i][0]
        password = data[i][1]
        if login_id == line_id:
            print('id found')
            if login_password == password:
                master.destroy  # need to be fixed
                acc_dashboard = Tk()
                acc_dashboard.title('Dashboard')
                return True
    print('id not found')
    return False


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
