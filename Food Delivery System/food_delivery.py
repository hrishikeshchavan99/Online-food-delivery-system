#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import random

root = tk.Tk()
root.resizable(0,0)
root.option_add('*Dialog.msg.font', 'Times 13 bold')
root.geometry('700x600+450+250')
root.title("Food delivery")

db = MySQLdb.connect("localhost","tushar","Tushar123","food_delivery")
cursor = db.cursor()

text_font = ('Times', '20')
bg_color = "#dbe64c"
root.configure(background=bg_color)

current_user = {'email':''}
current_delivery = {'email':''}
current_employee = {'email':''}
current_order = ()
items = set()
quantity = []
total_bill = 0

def order_summary(root):
    
    def order_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_user['email'] = ''
        global current_order
        current_order = ()
        customer_login(root)
    
    def order_menu():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        menu(root)

    def place_order():
        sql = "select count(*) from order1"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result[0][0] == 0:
            for i in range(len(items)):
                sql = "select foodid, price from food where foodname='{}'".format(items[i])
                cursor.execute(sql)
                result = cursor.fetchall()
                foodid = result[0][0]
                bill = quantity[i] * result[0][1]
                sql = "insert into order1 values ({}, '{}', {}, {}, {})".format(1, current_user['email'], foodid, quantity[i], bill)
                cursor.execute(sql)
                db.commit()
        else:
            sql = "select max(ordid) from order1"
            cursor.execute(sql)
            result = cursor.fetchall()
            orderid = result[0][0] + 1
            for i in range(len(items)):
                sql = "select foodid, price from food where foodname='{}'".format(items[i])
                cursor.execute(sql)
                result = cursor.fetchall()
                foodid = result[0][0]
                bill = quantity[i] * result[0][1]
                sql = "insert into order1 values ({}, '{}', {}, {}, {})".format(orderid, current_user['email'], foodid, quantity[i], bill)
                cursor.execute(sql)
                db.commit()
        messagebox.showinfo('Order', 'Order Placed Successfully')
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        order_details(root)
            
    def order_profile():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_profile(root)
    
    
    sql = "select name from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')
    
    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Order Summary", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=order_logout)
    button_1 = tk.Button(row, text="Profile", font="Aileron 10", command=order_profile)
    button.pack(anchor='ne', side=tk.RIGHT)
    button_1.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Items in Cart", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Listbox(row1, font="Times 20", height=3, width=30)
    row1.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Total Bill", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Listbox(row2, font="Times 20", height=1, width=30)
    row2.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Address", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Listbox(row3, font="Times 20", height=3, width=30)
    row3.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Date and time", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Listbox(row4, font="Times 20", height=1, width=30)

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")
    ent4.insert(0, dt_string)

    row4.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT)

    button_row1 = tk.Frame(root, bg=bg_color)
    button1 = tk.Button(button_row1, text="Place Order", font="Times 20", command=place_order)
    button2 = tk.Button(button_row1, text="Back", font="Times 20", command=order_menu)
    button_row1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=40)
    button1.pack(side=tk.RIGHT, padx=100)
    button2.pack(side=tk.LEFT, padx=100)

    global items
    items = set()
    global quantity
    quantity = []
    for i in current_order:
        items.add(i)

    items = list(items)
    for i in items:
        quantity.append(current_order.count(i))
    
    for i in range(len(items)):
        ent1.insert(i, items[i]+"      "+str(quantity[i]))
    
    sql = "select c_address from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    ent3.insert(0, result[0][0])
    
    global total_bill
    total_bill = 0
    for i in range(len(items)):
        sql = "select price from food where foodname='{}'".format(items[i])
        cursor.execute(sql)
        result = cursor.fetchall()
        total_bill = total_bill + quantity[i]*int(result[0][0])
    
    ent2.insert(0, str(total_bill))
    
    root.mainloop()
    return


def order_details(root):
    
    global current_order, items, quantity, total_bill
    def details_menu():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_order = ()
        menu(root)
    
    def details_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_user['email'] = ''
        global current_order
        current_order = ()
        customer_login(root)
    
    def details_profile():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_order = ()
        customer_profile(root)
    
    sql = "select name from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]
    
    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Order Details", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=details_logout)
    button_1 = tk.Button(row, text="Profile", font="Aileron 10", command=details_profile)
    button.pack(anchor='ne', side=tk.RIGHT)
    button_1.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Order ID", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Listbox(row1, font="Times 20", height=1)
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Items", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Listbox(row2, font="Times 20", height=4)
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Total bill", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Listbox(row3, font="Times 20", height=1)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Contact At", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Listbox(row4, font="Times 20", height=1)
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Time and Date", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Listbox(row5, font="Times 20", height=1)
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row6, text="Menu", font="Times 20", command=details_menu)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    button1.pack(anchor='n')
    
    sql = "select max(ordid) from order1"
    cursor.execute(sql)
    result = cursor.fetchall()
    orderid = result[0][0]
    
    sql = "select e_email, e_mobile from employee"
    cursor.execute(sql)
    result = cursor.fetchall()
    i = random.randint(0, len(result)-1)
    current_delivery['email'] = result[i][0]
    mob = result[i][1]
    
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")
    date = dt_string.split(' ')[0]
    time = dt_string.split(' ')[1]
    
    sql = "insert into delivery (ordid, c_email, e_email, delcharge, deldate, deltime) values({}, '{}', '{}', {}, '{}', '{}')".format(orderid, current_user['email'], current_delivery['email'], total_bill, date, time)
    cursor.execute(sql)
    db.commit()
    
    ent1.insert(0, str(orderid))
    
    for i in range(len(items)):
        ent2.insert(i, items[i]+"      "+str(quantity[i]))
    
    ent3.insert(0, total_bill)
    ent4.insert(0, mob)
    
    ent5.insert(0, dt_string)
    
    root.mainloop()
    return

def customer_history(root):
    
    index = 1
    def history_menu():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        menu(root)
    
    def history_profile():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_profile(root)
    
    def history_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_user['email'] = ''
        global current_order
        current_order = ()
        customer_login(root)
        
    def history_next():
        
        ent1.delete(0, tk.END)
        ent2.delete(0, tk.END)
        ent3.delete(0, tk.END)
        ent4.delete(0, tk.END)
        ent5.delete(0, tk.END)
        
        sql = "select ordid, e_email, delcharge, deldate, deltime from delivery where c_email='{}'".format(current_user['email'])
        cursor.execute(sql)
        result = cursor.fetchall()
        
        nonlocal index
        if index == len(result):
            index = 0
        
        orderid = result[index][0]
        e_email = result[index][1]
        bill = result[index][2]
        date = result[index][3]
        time = result[index][4]
        sql = "select foodid, quantity from order1 where ordid={}".format(orderid)
        cursor.execute(sql)
        result_c = cursor.fetchall()
        a = []
        for i in range(len(result_c)):
                foodid = result_c[i][0]
                quantity = result_c[i][1]
                sql = "select foodname from food where foodid={}".format(foodid)
                cursor.execute(sql)
                result_f = cursor.fetchall()
                a.append(result_f[0][0]+"    "+str(quantity))
        
        sql = "select name from employee where e_email='{}'".format(e_email)
        cursor.execute(sql)
        name = cursor.fetchall()
        
        ent1.insert(0, str(orderid))
        for i in a:
            ent2.insert(0, i)
        
        ent3.insert(0, str(bill))
        ent4.insert(0, name[0][0])
        ent5.insert(0, date+' '+time)
        
        index += 1
        
    
    sql = "select name from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Order History", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=history_logout)
    button_1 = tk.Button(row, text="Profile", font="Aileron 10", command=history_profile)
    button.pack(anchor='ne', side=tk.RIGHT)
    button_1.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Order ID", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Listbox(row1, font="Times 20", height=1)
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Items", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Listbox(row2, font="Times 20", height=4)
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Total bill", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Listbox(row3, font="Times 20", height=1)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Delivered by", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Listbox(row4, font="Times 20", height=1)
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Time and Date", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Listbox(row5, font="Times 20", height=1)
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row6, text="Menu", font="Times 20", command=history_menu)
    button2 = tk.Button(row6, text="Next", font="Times 20", command=history_next)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    button1.pack(side=tk.LEFT, padx=100)
    button2.pack(side=tk.RIGHT, padx=100)
    
    sql = "select ordid, e_email, delcharge, deldate, deltime from delivery where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if result:
        orderid = result[0][0]
        e_email = result[0][1]
        bill = result[0][2]
        date = result[0][3]
        time = result[0][4]
        sql = "select foodid, quantity from order1 where ordid={}".format(orderid)
        cursor.execute(sql)
        result_c = cursor.fetchall()
        a = []
        for i in range(len(result_c)):
                foodid = result_c[i][0]
                quantity = result_c[i][1]
                sql = "select foodname from food where foodid={}".format(foodid)
                cursor.execute(sql)
                result_f = cursor.fetchall()
                a.append(result_f[0][0]+"    "+str(quantity))
        
        sql = "select name from employee where e_email='{}'".format(e_email)
        cursor.execute(sql)
        name = cursor.fetchall()
        
        ent1.insert(0, str(orderid))
        for i in a:
            ent2.insert(0, i)
        
        ent3.insert(0, str(bill))
        ent4.insert(0, name[0][0])
        ent5.insert(0, date+' '+time)
    else:
        messagebox.showinfo('Employee', 'No Past Orders')

    root.mainloop()

def customer_profile(root):
    
    def profile_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_user['email'] = ''
        global current_order
        current_order = ()
        customer_login(root)
    
    def profile_menu():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        menu(root)
    
    def profile_history():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_history(root)
        
    def profile_save():
        name = ent1.get()
        mob = ent3.get()
        address = ent5.get("1.0", tk.END)
        address = address[:len(address)-1]
        password = ent6.get()
        c_password = ent7.get()
        
        if len(mob)==10:
            if password and c_password:
                if password == c_password:
                    sql = "update customer set name='{}', c_mobile='{}', c_address='{}', c_pass='{}' where c_email='{}'".format(name, mob, address, password, current_user['email'])
                    cursor.execute(sql)
                    db.commit()
                    messagebox.showinfo('Success', 'Record Saved Successfully')
                else:
                    messagebox.showerror('Error', 'Password does not match')
            else:
                sql = "update customer set name='{}', c_mobile='{}', c_address='{}' where c_email='{}'".format(name, mob, address, current_user['email'])
                cursor.execute(sql)
                db.commit()
                messagebox.showinfo('Success', 'Record Saved Successfully')
        else:
            messagebox.showerror('Error', 'Mobile number should be of 10 Digits')
            
    
    sql = "select name from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]
    
    
    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Profile", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=profile_logout)
    button.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Full Name", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Email", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Listbox(row2, font="Times 20", height=1, width=30)
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Mobile No", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Entry(row3, font="Times 20")
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Address", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Text(row5, font="Times 20", height=4)
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="New Password", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Entry(row6, font="Times 20", show='*')
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row7 = tk.Frame(root,bg=bg_color)
    lab7 = tk.Label(row7, width=20, text="Confirm Password", font="Times 20", anchor='w',bg=bg_color)
    ent7 = tk.Entry(row7, font="Times 20", show='*')
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab7.pack(side=tk.LEFT)
    ent7.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row8 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row8, text="Save", font="Times 20", command=profile_save)
    button2 = tk.Button(row8, text="Menu", font="Times 20", command=profile_menu)
    button3 = tk.Button(row8, text="Order_history", font="Times 20", command=profile_history)
    row8.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    button1.pack(side=tk.LEFT, padx=50)
    button2.pack(side=tk.RIGHT, padx=50)
    button3.pack(anchor='n')
    
    sql = "select * from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][1]
    address = result[0][3]
    mob = result[0][4]
    
    ent1.insert(0, name)
    ent2.insert(0, current_user['email'])
    ent3.insert(0, mob)
    ent5.insert("1.0", address)
    
    root.mainloop()
    return


def menu(root):
    
    global current_order
    
    def add_1():
        temp = ent1.get()
        if temp != "select":
            ent6.insert(1, temp)

    def add_2():
        temp = ent2.get()
        if temp != "select":
            ent6.insert(1, temp)

    def add_3():
        temp = ent3.get()
        if temp != "select":
            ent6.insert(1, temp)

    def add_4():
        temp = ent4.get()
        if temp != "select":
            ent6.insert(1, temp)

    def add_5():
        temp = ent5.get()
        if temp != "select":
            ent6.insert(1, temp)

    def delete_item():
        if ent6.get(tk.ACTIVE) != "Selected Items:-":
            ent6.delete(tk.ACTIVE)

    def total_items():
        global current_order
        current_order = ent6.get(1, tk.END)
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        order_summary(root)
        
    def menu_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_user['email'] = ''
        global current_order
        current_order = ()
        customer_login(root)
    
    def menu_profile():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_profile(root)

    text_font = ('Times', '20')
    root.configure(background=bg_color)
    
    sql = "select name from customer where c_email='{}'".format(current_user['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]
    
    l_main = []
    sql = "select foodname from food where categery='main'"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        l_main.append(result[i][0])
    
    l_roti = []
    sql = "select foodname from food where categery='roti'"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        l_roti.append(result[i][0])
    
    l_rice = []
    sql = "select foodname from food where categery='rice'"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        l_rice.append(result[i][0])
    
    l_fast = []
    sql = "select foodname from food where categery='fast'"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        l_fast.append(result[i][0])
    
    l_desert = []
    sql = "select foodname from food where categery='desert'"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        l_desert.append(result[i][0])

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')
    
    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Menu", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=menu_logout)
    button_1 = tk.Button(row, text="Profile", font="Aileron 10", command=menu_profile)
    button.pack(anchor='ne', side=tk.RIGHT)
    button_1.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Main Course", font="Times 20", anchor='w',bg=bg_color)
    ent1 = ttk.Combobox(row1, values=l_main, font=text_font, width=15, state='readonly')
    ent1.set("select")
    button1 = tk.Button(row1, text="ADD", font="Times 20", command=add_1)
    row1.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.LEFT)
    button1.pack(side=tk.RIGHT)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Roti/Naan", font="Times 20", anchor='w',bg=bg_color)
    ent2 = ttk.Combobox(row2, values=l_roti, font=text_font, width=15, state='readonly')
    ent2.set("select")
    button2 = tk.Button(row2, text="ADD", font="Times 20", command=add_2)
    row2.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.LEFT)
    button2.pack(side=tk.RIGHT)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Rice", font="Times 20", anchor='w',bg=bg_color)
    ent3 = ttk.Combobox(row3, values=l_rice, font=text_font, width=15, state='readonly')
    ent3.set("select")
    button3 = tk.Button(row3, text="ADD", font="Times 20", command=add_3)
    row3.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.LEFT)
    button3.pack(side=tk.RIGHT)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Fast Food", font="Times 20", anchor='w',bg=bg_color)
    ent4 = ttk.Combobox(row4, values=l_fast, font=text_font, width=15, state='readonly')
    ent4.set("select")
    button4 = tk.Button(row4, text="ADD", font="Times 20", command=add_4)
    row4.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.LEFT)
    button4.pack(side=tk.RIGHT)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Desert/Bevereges", font="Times 20", anchor='w',bg=bg_color)
    ent5 = ttk.Combobox(row5, values=l_desert, font=text_font, width=15, state='readonly')
    ent5.set("select")
    button5 = tk.Button(row5, text="ADD", font="Times 20", command=add_5)
    row5.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.LEFT)
    button5.pack(side=tk.RIGHT)

    row6 = tk.Frame(root,bg=bg_color)
    ent6 = tk.Listbox(row6, font="Times 20", height=6, width=20)
    ent6.insert(0, "Selected Items:-")
    button6 = tk.Button(row6, text="ADD to Cart", font="Times 20", command=total_items)
    button7 = tk.Button(row6, text="Remove", font="Times 20", command=delete_item)
    row6.pack(side=tk.TOP, fill=tk.X,padx=15, pady=10)
    button6.pack(side=tk.RIGHT)
    ent6.pack(side=tk.LEFT)
    button7.pack(side=tk.LEFT, padx=15)
    
    if current_order:
        for i in current_order:
            ent6.insert(1, i)

    root.mainloop()
    return


def customer_signup(root):
    
    def signup_signup():
        
        name = ent1.get()
        email = ent2.get()
        mob = ent3.get()
        password = ent4.get()
        c_password = ent5.get()
        address = ent6.get("1.0",tk.END)
        address = address[:len(address)-1]
        
        if name and email and mob and password and c_password and address:
            if password == c_password:
                if len(mob) != 10:
                    messagebox.showerror('Sign up error', 'Mobile No. Should be of 10 Digits')
                else:
                    try:
                        sql = "insert into customer values ('{}', '{}', '{}', '{}', '{}')".format(email, name, password, address, mob)
                        cursor.execute(sql)
                        db.commit()
                        messagebox.showinfo('Sign up message', 'Successfully Registered');
                        info = root.winfo_children()
                        for i in range(len(info)):
                            info[i].destroy()
                        current_user['email'] = email
                        menu(root)
                    
                    except:
                        messagebox.showerror('Sign up error', 'Account already exist')
                        ent1.delete(0,tk.END)
                        ent2.delete(0,tk.END)
                        ent3.delete(0,tk.END)
                        ent4.delete(0,tk.END)
                        ent5.delete(0,tk.END)
                        ent6.delete("1.0",tk.END)
            else:
                messagebox.showerror('Sign up error', 'Password Dont Match')
                    
        else:
            messagebox.showwarning('Sign up Warning', 'All fields are mandatory')

    def signup_login():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_login(root)
    
    root.configure(background=bg_color)

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Create Account", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Full Name", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Email", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Mobile No", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Entry(row3, font="Times 20")
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Password", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Entry(row4, font="Times 20",show="*")
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Confirm Password", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Entry(row5, font="Times 20",show="*")
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="Address", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Text(row6, font="Times 20", height=4)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)


    button_row1 = tk.Frame(root, bg=bg_color)
    button1 = tk.Button(button_row1, text="Sign up", font="Times 20", command=signup_signup)
    button_row1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=15)
    button1.pack(anchor='n')

    row7 = tk.Frame(root,bg=bg_color)
    lab7 = tk.Label(row7, width=20, text="Already have an account", font="Times 20", anchor='w',bg=bg_color)
    button2 = tk.Button(row7, text="Login", font="Times 20", command=signup_login)
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=2)
    lab7.pack(side=tk.LEFT)
    button2.pack(side=tk.LEFT)

    root.mainloop()
    return


def add_food(root):
    
    def f_add():
        
        f_id = ent1.get()
        f_name = ent2.get()
        category = ent3.get()
        price = ent4.get()
        
        if f_id and f_name and category and price:
            try:
                sql = "insert into food values ({}, '{}', '{}', {})".format(f_id, f_name, category, price)
                cursor.execute(sql)
                db.commit()
                messagebox.showinfo('ADD message', 'Successfully Added');
                ent1.delete(0,tk.END)
                ent2.delete(0,tk.END)
                ent3.delete(0,tk.END)
                ent4.delete(0,tk.END)

            except:
                messagebox.showerror('ADD error', 'Food already exists')
                ent1.delete(0,tk.END)
                ent2.delete(0,tk.END)
                ent3.delete(0,tk.END)
                ent4.delete(0,tk.END)
                    
        else:
            messagebox.showwarning('ADD Warning', 'All fields are mandatory')

    def f_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update(root)
    
    root.configure(background=bg_color)

    name="Admin id:-100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Add Food", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Food ID", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Food name", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Food Category", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Entry(row3, font="Times 20")
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Price", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Entry(row4, font="Times 20")
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row6, text="ADD", font="Times 20", command=f_add)
    button2 = tk.Button(row6, text="Back", font="Times 20", command=f_back)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    button1.pack(side=tk.RIGHT, padx=100)
    button2.pack(side=tk.LEFT, padx=100)

    root.mainloop()
    return


def add_employee(root):
    
    def add():
        
        name = ent1.get()
        email = ent2.get()
        mob = ent3.get()
        password = ent4.get()
        c_password = ent5.get()
        address = ent6.get("1.0",tk.END)
        address = address[:len(address)-1]
        dob = ent7.get()
        salary = ent8.get()
        
        if name and email and mob and password and c_password and address and salary and dob:
            if password == c_password:
                if len(mob) != 10:
                    messagebox.showerror('ADD error', 'Mobile No. Should be of 10 Digits')
                else:
                    try:
                        sql = "insert into employee values ('{}', '{}', '{}', '{}', '{}','{}',{})".format(email, name, dob, password, address, mob, salary)
                        cursor.execute(sql)
                        db.commit()
                        messagebox.showinfo('ADD message', 'Successfully Added');
                        ent1.delete(0,tk.END)
                        ent2.delete(0,tk.END)
                        ent3.delete(0,tk.END)
                        ent4.delete(0,tk.END)
                        ent5.delete(0,tk.END)
                        ent6.delete("1.0",tk.END)
                        ent7.delete(0,tk.END)
                        ent8.delete(0,tk.END)
                    
                    except:
                        messagebox.showerror('ADD error', 'Account already exist')
                        ent1.delete(0,tk.END)
                        ent2.delete(0,tk.END)
                        ent3.delete(0,tk.END)
                        ent4.delete(0,tk.END)
                        ent5.delete(0,tk.END)
                        ent6.delete("1.0",tk.END)
                        ent7.delete(0,tk.END)
                        ent8.delete(0,tk.END)
            else:
                messagebox.showerror('ADD error', 'Password Does not Match')
                    
        else:
            messagebox.showwarning('ADD Warning', 'All fields are mandatory')

    def back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update(root)
    
    root.configure(background=bg_color)
    
    name="Admin id:-100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')
    
    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Add Employee", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Full Name", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Email", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Mobile No", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Entry(row3, font="Times 20")
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Password", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Entry(row4, font="Times 20",show="*")
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Confirm Password", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Entry(row5, font="Times 20",show="*")
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="Address", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Text(row6, font="Times 20", height=3)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row7 = tk.Frame(root,bg=bg_color)
    lab7 = tk.Label(row7, width=20, text="Date of Birth", font="Times 20", anchor='w',bg=bg_color)
    ent7 = tk.Entry(row7, font="Times 20")
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab7.pack(side=tk.LEFT)
    ent7.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row8 = tk.Frame(root,bg=bg_color)
    lab8 = tk.Label(row8, width=20, text="Salary", font="Times 20", anchor='w',bg=bg_color)
    ent8 = tk.Entry(row8, font="Times 20")
    row8.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab8.pack(side=tk.LEFT)
    ent8.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row9 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row9, text="ADD", font="Times 20", command=add)
    button2 = tk.Button(row9, text="Back", font="Times 20", command=back)
    row9.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    button1.pack(side=tk.RIGHT, padx=100)
    button2.pack(side=tk.LEFT, padx=100)

    root.mainloop()
    return


def search_order(root):
    
    index = 0
    index_2 = 0
    def search_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update(root)
    
    def search_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        admin_login(root)
    
    def search_search():
        
        nonlocal index, index_2
        
        select = combo.get()
        value = ent1.get()
        
        ent3.delete(0, tk.END)
        ent4.delete(0, tk.END)
        ent6.delete(0, tk.END)
        ent7.delete(0, tk.END)
        ent8.delete(0, tk.END)
        
        if select == "select":
            messagebox.showwarning('Warning', "Please Select Search by Value")
        else:
            if value:
                if select == "Order ID":
                    sql = "select c_email, e_email, delcharge, deldate, deltime from delivery where ordid={}".format(int(value))
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result):
                        c_email = result[0][0]
                        e_email = result[0][1]
                        bill = result[0][2]
                        time = result[0][3]+" "+result[0][4]

                        sql = "select foodid, quantity from order1 where ordid={}".format(int(value))
                        cursor.execute(sql)
                        result_c = cursor.fetchall()
                        a = []
                        for i in range(len(result_c)):
                                foodid = result_c[i][0]
                                quantity = result_c[i][1]
                                sql = "select foodname from food where foodid={}".format(foodid)
                                cursor.execute(sql)
                                result_f = cursor.fetchall()
                                a.append(result_f[0][0]+"    "+str(quantity))

                        sql = "select name from customer where c_email='{}'".format(c_email)
                        cursor.execute(sql)
                        result_c = cursor.fetchall()
                        name = result_c[0][0]

                        ent3.insert(0, name)
                        for i in a:
                            ent4.insert(0, i)
                        ent6.insert(0, str(bill))
                        ent7.insert(0, e_email)
                        ent8.insert(0, time)
                    else:
                        messagebox.showinfo("Info", "No Order with Order ID = {}".format(value))
                
                elif select == "Date":
                    sql = "select c_email, e_email, delcharge, deldate, deltime, ordid from delivery where deldate='{}'".format(value)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result):
                        if index>=len(result):
                            index = 0
                        c_email = result[index][0]
                        e_email = result[index][1]
                        bill = result[index][2]
                        time = result[index][3]+" "+result[index][4]
                        orderid = result[index][5]
                        
                        sql = "select foodid, quantity from order1 where ordid={}".format(orderid)
                        cursor.execute(sql)
                        result_c = cursor.fetchall()
                        a = []
                        for i in range(len(result_c)):
                                foodid = result_c[i][0]
                                quantity = result_c[i][1]
                                sql = "select foodname from food where foodid={}".format(foodid)
                                cursor.execute(sql)
                                result_f = cursor.fetchall()
                                a.append(result_f[0][0]+"    "+str(quantity))

                        sql = "select name from customer where c_email='{}'".format(c_email)
                        cursor.execute(sql)
                        result_c = cursor.fetchall()
                        name = result_c[0][0]

                        ent3.insert(0, name)
                        for i in a:
                            ent4.insert(0, i)
                        ent6.insert(0, str(bill))
                        ent7.insert(0, e_email)
                        ent8.insert(0, time)
                        index += 1
                    else:
                        messagebox.showinfo("Info", "No Order for {}".format(value))
                else:
                    sql = "select name, c_email, c_address from customer"
                    cursor.execute(sql)
                    result_d = cursor.fetchall()
                    result = []
                    for i in result_d:
                        if i[2].find(value) != -1:
                            result.append(i)
                    if index >= len(result):
                        index = 0
                        index_2 = 0
                    if len(result):
                        name = result[index][0]
                        c_email = result[index][1]
                        
                        sql = "select e_email, delcharge, deldate, deltime, ordid from delivery where c_email='{}'".format(c_email)
                        cursor.execute(sql)
                        result_c = cursor.fetchall()
                        
                        if len(result_c):
                            if len(result_c) <= index_2:
                                index_2 = 0
                                index += 1
                            else:    
                                e_email = result_c[index_2][0]
                                bill = result_c[index_2][1]
                                time = result_c[index_2][2]+" "+result_c[index_2][3]
                                orderid = result_c[index_2][4]

                                sql = "select foodid, quantity from order1 where ordid={}".format(orderid)
                                cursor.execute(sql)
                                result_c = cursor.fetchall()
                                a = []
                                for i in range(len(result_c)):
                                        foodid = result_c[i][0]
                                        quantity = result_c[i][1]
                                        sql = "select foodname from food where foodid={}".format(foodid)
                                        cursor.execute(sql)
                                        result_f = cursor.fetchall()
                                        a.append(result_f[0][0]+"    "+str(quantity))

                                ent3.insert(0, name)
                                for i in a:
                                    ent4.insert(0, i)
                                ent6.insert(0, str(bill))
                                ent7.insert(0, e_email)
                                ent8.insert(0, time)
                                index_2 += 1
                        else:
                            index += 1
                            index_2 = 0
                    else:
                        messagebox.showinfo("Info", "No Orders for area {}".format(value))
            else:
                messagebox.showwarning("Warning", "Please enter Value")

    
    name="Admin Id 100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Search Order", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=search_logout)
    button.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Search by", font="Times 20", anchor='w',bg=bg_color)
    combo = ttk.Combobox(row1, values=["Order ID", "Date", "Pincode"], font=text_font, width=8, state='readonly')
    combo.set("select")
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    combo.pack(side=tk.LEFT, padx=20)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row2, text="Back", font="Times 20", command=search_back)
    button2 = tk.Button(row2, text="Search/Next", font="Times 20", command=search_search)
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    button1.pack(side=tk.LEFT, padx=100)
    button2.pack(side=tk.RIGHT, padx=100)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Customer Name", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Listbox(row3, font="Times 20", height=1)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Items", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Listbox(row4, font="Times 20", height=4)
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="Total bill", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Listbox(row6, font="Times 20", height=1)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row7 = tk.Frame(root,bg=bg_color)
    lab7 = tk.Label(row7, width=20, text="Employee ID", font="Times 20", anchor='w',bg=bg_color)
    ent7 = tk.Listbox(row7, font="Times 20", height=1)
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab7.pack(side=tk.LEFT)
    ent7.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row8 = tk.Frame(root,bg=bg_color)
    lab8 = tk.Label(row8, width=20, text="Time and Date", font="Times 20", anchor='w',bg=bg_color)
    ent8 = tk.Listbox(row8, font="Times 20", height=1)
    row8.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab8.pack(side=tk.LEFT)
    ent8.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    root.mainloop()
    return


def update_food(root):

    def food_view_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update(root)

    def food_view():
        fid = ent.get()
        if fid:
            sql = "select * from food where foodid={}".format(fid)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                ent2.delete(0,tk.END)
                ent3.delete(0,tk.END)
                ent4.delete(0,tk.END)
                
                ent2.insert(0,result[0][1])
                ent3.insert(0,result[0][2])
                ent4.insert(0,str(result[0][3]))
            else:
                messagebox.showinfo("Info", "No recoed Found")
        else:
            messagebox.showwarning("Warning", "Food Id can't be empty")

    def food_save():
        fid = ent.get()
        if fid:
            name = ent2.get()
            category = ent3.get()
            price = ent4.get()

            sql = "update food set foodname='{}', categery='{}', price={} where foodid={}".format(name, category, price, fid)
            cursor.execute(sql)
            db.commit()
            messagebox.showinfo('Success', 'Record Saved Successfully')
        else:
            messagebox.showwarning("Warning", "Food Id can't be empty")


    name="Admin ID:- 100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=20, text="Food ID", font="Times 20", anchor='w',bg=bg_color)
    ent = tk.Entry(row, font="Times 20")
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row1 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row1, text="View", font="Times 20", command=food_view)
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    button1.pack(anchor='n')

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Food Name", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Category", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Entry(row3, font="Times 20")
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Price", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Entry(row4, font="Times 20")
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row9 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row9, text="Save", font="Times 20", command=food_save)
    button2 = tk.Button(row9, text="Back", font="Times 20", command=food_view_back)
    row9.pack(side=tk.TOP, fill=tk.X,padx=5, pady=15)
    button1.pack(side=tk.RIGHT, padx=100)
    button2.pack(side=tk.LEFT, padx=100)

    root.mainloop()
    return

def update_employee(root):

    def employee_view_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update(root)

    def employee_view():
        email = ent.get()
        if email:
            sql = "select * from employee where e_email='{}'".format(email)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                ent2.delete(0,tk.END)
                ent3.delete(0,tk.END)
                ent4.delete(0,tk.END)
                ent5.delete(0,tk.END)
                ent6.delete("1.0",tk.END)
                ent7.delete(0,tk.END)
                ent8.delete(0,tk.END)
                
                ent2.insert(0,result[0][1])
                ent3.insert(0,result[0][2])
                ent6.insert("1.0",result[0][4])
                ent7.insert(0,result[0][5])
                ent8.insert(0,str(result[0][6]))
            else:
                messagebox.showinfo("Info", "No record Found")
        else:
            messagebox.showwarning("Warning", "Email can't be empty")

    def employee_save():
        email = ent.get()
        if email:
            name = ent2.get()
            date = ent3.get()
            password = ent4.get()
            c_password = ent5.get()
            address = ent6.get("1.0",tk.END)
            address = address[:len(address)-1]
            mob = ent7.get()
            salary = ent8.get()

            if len(mob)==10:
                if password and c_password:
                    if password == c_password:
                        sql = "update employee set name='{}', e_mobile='{}', e_address='{}', e_pass='{}', dob='{}', salary='{}' where e_email='{}'".format(name, mob, address, password, date, salary, email)
                        cursor.execute(sql)
                        db.commit()
                        messagebox.showinfo('Success', 'Record Saved Successfully')
                    else:
                        messagebox.showerror('Error', 'Password does not match')
                else:
                    sql = "update employee set name='{}', e_mobile='{}', e_address='{}', dob='{}', salary='{}' where e_email='{}'".format(name, mob, address, date, salary, email)
                    cursor.execute(sql)
                    db.commit()
                    messagebox.showinfo('Success', 'Record Saved Successfully')
            else:
                messagebox.showerror('Error', 'Mobile number should be of 10 Digits')
        else:
            messagebox.showwarning("Warning", "Email can't be empty")


    name="Admin ID:- 100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=20, text="Email", font="Times 20", anchor='w',bg=bg_color)
    ent = tk.Entry(row, font="Times 20")
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row1 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row1, text="View", font="Times 20", command=employee_view)
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    button1.pack(anchor='n')

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Full Name", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="DOB", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Entry(row3, font="Times 20")
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Password", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Entry(row4, font="Times 20",show="*")
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Confirm Password", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Entry(row5, font="Times 20",show="*")
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="Address", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Text(row6, font="Times 20", height=3)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row7 = tk.Frame(root,bg=bg_color)
    lab7 = tk.Label(row7, width=20, text="Mobile", font="Times 20", anchor='w',bg=bg_color)
    ent7 = tk.Entry(row7, font="Times 20")
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab7.pack(side=tk.LEFT)
    ent7.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row8 = tk.Frame(root,bg=bg_color)
    lab8 = tk.Label(row8, width=20, text="Salary", font="Times 20", anchor='w',bg=bg_color)
    ent8 = tk.Entry(row8, font="Times 20")
    row8.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    lab8.pack(side=tk.LEFT)
    ent8.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row9 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row9, text="Save", font="Times 20", command=employee_save)
    button2 = tk.Button(row9, text="Back", font="Times 20", command=employee_view_back)
    row9.pack(side=tk.TOP, fill=tk.X,padx=5, pady=5)
    button1.pack(side=tk.RIGHT, padx=100)
    button2.pack(side=tk.LEFT, padx=100)

    root.mainloop()
    return


def delete(root):
    
    def delete_delete():
        select = ent1.get()
        d_id = ent2.get()
        if select == "select":
            messagebox.showwarning("Warning", "Please Select Food/Employee")
        else:
            if d_id:
                if select == "Food":
                    sql = "delete from food where foodid={}".format(d_id)
                else:
                    sql = "delete from employee where e_email='{}'".format(d_id)
                
                try:
                    cursor.execute(sql)
                    db.commit()
                    messagebox.showinfo("Success", "{} Successfully Deleted".format(select))
                except:
                    messagebox.showerror("Error", "Enter Valid Integer food id")
            else:
                messagebox.showwarning("Warning", "Please Enter {} Id".format(select))

    def delete_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update(root)

    name="Admin Id:-100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Delete Employee/Food", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=20)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Delete", font="Times 20", anchor='w',bg=bg_color)
    ent1 = ttk.Combobox(row1, values=["Employee", "Food"], font=text_font, width=8, state='readonly')
    ent1.set("select")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="ID", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row3, text="Delete", font="Times 20", command=delete_delete)
    button2 = tk.Button(row3, text="Back", font="Times 20", command=delete_back)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)
    button1.pack(side=tk.RIGHT, padx=100)
    button2.pack(side=tk.LEFT, padx=100)

    root.mainloop()
    return


def update(root):
    
    def update_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        admin_login(root)
    
    def update_add_e():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        add_employee(root)
    
    def update_add_f():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        add_food(root)
    
    def update_order():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        search_order(root)
    
    def update_e():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update_employee(root)
    
    def update_f():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        update_food(root)
    
    def update_d():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        delete(root)
    
    name="Admin id:-100"

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Times 10", command=update_logout)
    button.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)

    row1 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row1, text="ADD Employee", font="Times 20", command=update_add_e)
    button1.pack(anchor='n')
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)

    row2 = tk.Frame(root,bg=bg_color)
    button2 = tk.Button(row2, text="Update/View Employee", font="Times 20", command=update_e)
    button2.pack(anchor='n')
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)

    row3 = tk.Frame(root,bg=bg_color)
    button3 = tk.Button(row3, text="ADD Food", font="Times 20", command=update_add_f)
    button3.pack(anchor='n')
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)

    row4 = tk.Frame(root,bg=bg_color)
    button4 = tk.Button(row4, text="Update/View Food", font="Times 20", command=update_f)
    button4.pack(anchor='n')
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)

    row5 = tk.Frame(root,bg=bg_color)
    button5 = tk.Button(row5, text="Search Order", font="Times 20", command=update_order)
    button5.pack(anchor='n')
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)
    
    row6 = tk.Frame(root,bg=bg_color)
    button6 = tk.Button(row6, text="Delete Food/Employee", font="Times 20", command=update_d)
    button6.pack(anchor='n')
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=20)


    root.mainloop()


def admin_login(root):
    
    def admin_login():
        admin_id = ent1.get()
        password = ent2.get()
        
        if admin_id and password:
            sql = "select count(*) from admin where admin_ID={}".format(admin_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result[0][0] == 1:
                sql = "select a_pass from admin where admin_ID={}".format(admin_id)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result[0][0] == password:
                    info = root.winfo_children()
                    for i in range(len(info)):
                        info[i].destroy()
                    update(root)
                else:
                    messagebox.showerror('Login Error', 'Incorrect Password')

            else:
                messagebox.showerror('Login Error', 'Incorrect ID')
        else:
            messagebox.showwarning('Login Warning', 'ID or Password Cannot be empty')
    
    def admin_customer():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_login(root)
    
    def admin_employee():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        employee_login(root)
    
    root.configure(background=bg_color)

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Admin Login", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=20)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Admin id", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Password", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20",show="*")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    button_row1 = tk.Frame(root, bg=bg_color)
    button1 = tk.Button(button_row1, text="Login", font="Times 20", command=admin_login)
    button_row1.pack(side=tk.TOP, fill=tk.X, padx=100, pady=25)
    button1.pack(anchor='n')

    button_row2 = tk.Frame(root, bg=bg_color)
    button4 = tk.Button(button_row2, text="Customer", font="Times 20", command=admin_customer)
    button5 = tk.Button(button_row2, text="Employee", font="Times 20", command=admin_employee)
    button_row2.pack(side=tk.TOP, fill=tk.X, padx=100, pady=25)
    button4.pack(side=tk.LEFT)
    button5.pack(side=tk.RIGHT)

    root.mainloop()
    return

def employee_past(root):
    
    index = 1
    def past_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_employee['email'] = ""
        employee_login(root)
    
    def past_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        employee_page(root)
    
    def past_next():
        ent1.delete(0, tk.END)
        ent2.delete(0, tk.END)
        ent3.delete(0, tk.END)
        ent4.delete(0, tk.END)
        ent5.delete(0, tk.END)
        ent6.delete(0, tk.END)
        
        sql = "select ordid, c_email, delcharge, deldate, deltime from delivery where e_email='{}'".format(current_employee['email'])
        cursor.execute(sql)
        result = cursor.fetchall()
        
        nonlocal index
        
        if index == len(result):
            index = 0
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M")
        c_date = dt_string.split(' ')[0]
        c_time = dt_string.split(' ')[1]
        
        orderid = result[index][0]
        c_email = result[index][1]
        bill = result[index][2]
        date = result[index][3]
        time = result[index][4]
        sql = "select name, c_mobile, c_address from customer where c_email='{}'".format(c_email)
        cursor.execute(sql)
        result_c = cursor.fetchall()
        name = result_c[0][0]
        mob = result_c[0][1]
        address = result_c[0][2]
                            
        ent1.insert(0, str(orderid))
        ent2.insert(0, name)
        ent3.insert(0, mob)
        ent4.insert(0, str(bill))
        ent5.insert(0, date+' '+time)
        ent6.insert(0, address)
        
        index += 1
    
    sql = "select name from employee where e_email='{}'".format(current_employee['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Past Orders", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=past_logout)
    button.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Order ID", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Listbox(row1, font="Times 20", height=1)
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Customer Name", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Listbox(row2, font="Times 20", height=1)
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Mobile", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Listbox(row3, font="Times 20", height=1)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Total bill", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Listbox(row4, font="Times 20", height=1)
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Time and Date", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Listbox(row5, font="Times 20", height=1)
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="Delivery Adress", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Listbox(row6, font="Times 20", height=4)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row7 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row7, text="Back", font="Times 20", command=past_back)
    button2 = tk.Button(row7, text="Next", font="Times 20", command=past_next)
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    button1.pack(side=tk.LEFT, padx=100)
    button2.pack(side=tk.RIGHT, padx=100)
    
    sql = "select ordid, c_email, delcharge, deldate, deltime from delivery where e_email='{}'".format(current_employee['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")
    c_date = dt_string.split(' ')[0]
    c_time = dt_string.split(' ')[1]
    if result:
        orderid = result[0][0]
        c_email = result[0][1]
        bill = result[0][2]
        date = result[0][3]
        time = result[0][4]
        sql = "select name, c_mobile, c_address from customer where c_email='{}'".format(c_email)
        cursor.execute(sql)
        result_c = cursor.fetchall()
        name = result_c[0][0]
        mob = result_c[0][1]
        address = result_c[0][2]
                            
        ent1.insert(0, str(orderid))
        ent2.insert(0, name)
        ent3.insert(0, mob)
        ent4.insert(0, str(bill))
        ent5.insert(0, date+' '+time)
        ent6.insert(0, address)
    else:
        messagebox.showinfo('Employee', 'No Past Orders')

    root.mainloop()
    return

def employee_current(root):
    
    def current_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_employee['email'] = ""
        employee_login(root)
    
    def current_back():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        employee_page(root)
    
    sql = "select name from employee where e_email='{}'".format(current_employee['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Current order", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Aileron 10", command=current_logout)
    button.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Order ID", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Listbox(row1, font="Times 20", height=1)
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Customer Name", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Listbox(row2, font="Times 20", height=1)
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Mobile", font="Times 20", anchor='w',bg=bg_color)
    ent3 = tk.Listbox(row3, font="Times 20", height=1)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab3.pack(side=tk.LEFT)
    ent3.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row4 = tk.Frame(root,bg=bg_color)
    lab4 = tk.Label(row4, width=20, text="Total bill", font="Times 20", anchor='w',bg=bg_color)
    ent4 = tk.Listbox(row4, font="Times 20", height=1)
    row4.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab4.pack(side=tk.LEFT)
    ent4.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row5 = tk.Frame(root,bg=bg_color)
    lab5 = tk.Label(row5, width=20, text="Time and Date", font="Times 20", anchor='w',bg=bg_color)
    ent5 = tk.Listbox(row5, font="Times 20", height=1)
    row5.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab5.pack(side=tk.LEFT)
    ent5.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row6 = tk.Frame(root,bg=bg_color)
    lab6 = tk.Label(row6, width=20, text="Delivery Adress", font="Times 20", anchor='w',bg=bg_color)
    ent6 = tk.Listbox(row6, font="Times 20", height=4)
    row6.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab6.pack(side=tk.LEFT)
    ent6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row7 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row7, text="Back", font="Times 20", command=current_back)
    row7.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    button1.pack(anchor='n')
    
    sql = "select ordid, c_email, delcharge, deldate, deltime from delivery where e_email='{}'".format(current_employee['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    
    temp = False
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")
    c_date = dt_string.split(' ')[0]
    c_time = dt_string.split(' ')[1]
    if result:
        for i in range(len(result)):
            orderid = result[i][0]
            c_email = result[i][1]
            bill = result[i][2]
            date = result[i][3]
            time = result[i][4]
            if int(date[5:7])-int(c_date[5:7]) == 0:
                if int(date[8:])-int(c_date[8:]) == 0:
                    if int(time[0:2])-int(c_time[0:2]) == 0:
                        if abs(int(time[3:])-int(c_time[3:])) <=20:
                            sql = "select name, c_mobile, c_address from customer where c_email='{}'".format(c_email)
                            cursor.execute(sql)
                            result_c = cursor.fetchall()
                            name = result_c[0][0]
                            mob = result_c[0][1]
                            address = result_c[0][2]
                            temp = True
                            break
        if temp:
            ent1.insert(0, str(orderid))
            ent2.insert(0, name)
            ent3.insert(0, mob)
            ent4.insert(0, str(bill))
            ent5.insert(0, date+' '+time)
            ent6.insert(0, address)
        else:
            messagebox.showinfo('Employee', 'No Current Orders')
    else:
        messagebox.showinfo('Employee', 'No Current Orders')

    root.mainloop()
    return

def employee_page(root):
    
    def page_logout():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        current_employee['email'] = ""
        employee_login(root)
    
    def page_profile():
        pass
    
    def page_current():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        employee_current(root)
    
    def page_previous():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        employee_past(root)
    
    sql = "select name from employee where e_email='{}'".format(current_employee['email'])
    cursor.execute(sql)
    result = cursor.fetchall()
    name = result[0][0]

    row0 = tk.Frame(root, bg=bg_color)
    lab0 = tk.Label(row0, width=len(name), text=name, font="Aileron 15", anchor='n', fg="chocolate", bg=bg_color)
    row0.pack(side=tk.TOP, fill="both")
    lab0.pack(anchor='se')

    row = tk.Frame(root, bg=bg_color)
    button = tk.Button(row, text="LogOut", font="Times 10", command=page_logout)
    button.pack(anchor='ne', side=tk.RIGHT)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=15)

    row4 = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row4, width=27, text="Employee", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    lab.pack(anchor='n')
    row4.pack(side=tk.TOP, fill="both",padx=5, pady=15)

    row1 = tk.Frame(root,bg=bg_color)
    button1 = tk.Button(row1, text="Profile", font="Times 20", command=page_profile)
    button1.pack(anchor='n')
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=25)

    row2 = tk.Frame(root,bg=bg_color)
    button2 = tk.Button(row2, text="Current Order", font="Times 20", command=page_current)
    button2.pack(anchor='n')
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=25)

    row3 = tk.Frame(root,bg=bg_color)
    button3 = tk.Button(row3, text="Previous Orders", font="Times 20", command=page_previous)
    button3.pack(anchor='n')
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=25)

    root.mainloop()


def employee_login(root):
    
    def employee_log():
        email = ent1.get()
        password = ent2.get()
        
        if email and password:
            sql = "select count(*) from employee where e_email='{}'".format(email)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result[0][0] == 1:
                sql = "select e_pass from employee where e_email='{}'".format(email)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result[0][0] == password:
                    info = root.winfo_children()
                    for i in range(len(info)):
                        info[i].destroy()
                    current_employee['email'] = email
                    employee_page(root)
                else:
                    messagebox.showerror('Login Error', 'Incorrect Password')

            else:
                messagebox.showerror('Login Error', 'Incorrect email')
        else:
            messagebox.showwarning('Login Warning', 'Email or Password Cannot be empty')
    
    def employee_customer():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_login(root)
    
    def employee_admin():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        admin_login(root)
    
    root.configure(background=bg_color)

    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Employee Login", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=20)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Employee id", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Password", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20",show="*")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    button_row1 = tk.Frame(root, bg=bg_color)
    button1 = tk.Button(button_row1, text="Login", font="Times 20", command=employee_log)
    button_row1.pack(side=tk.TOP, fill=tk.X, padx=100, pady=25)
    button1.pack(anchor='n')

    button_row2 = tk.Frame(root, bg=bg_color)
    button4 = tk.Button(button_row2, text="Customer", font="Times 20", command=employee_customer)
    button5 = tk.Button(button_row2, text="Admin", font="Times 20", command=employee_admin)
    button_row2.pack(side=tk.TOP, fill=tk.X, padx=100, pady=25)
    button4.pack(side=tk.LEFT)
    button5.pack(side=tk.RIGHT)

    root.mainloop()
    return

def customer_login(root):
    
    def login():
        email = ent1.get()
        password = ent2.get()
        
        if email and password:
            sql = "select count(*) from customer where c_email='{}'".format(email)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result[0][0] == 1:
                sql = "select c_pass from customer where c_email='{}'".format(email)
                cursor.execute(sql)
                result = cursor.fetchall()
                if result[0][0] == password:
                    info = root.winfo_children()
                    for i in range(len(info)):
                        info[i].destroy()
                    current_user['email'] = email
                    menu(root)
                else:
                    messagebox.showerror('Login Error', 'Incorrect Password')

            else:
                messagebox.showerror('Login Error', 'Incorrect email')
        else:
            messagebox.showwarning('Login Warning', 'Email or Password Cannot be empty')
            
    
    def signup():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        customer_signup(root)
    
    def employee():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        employee_login(root)
        
    def admin():
        info = root.winfo_children()
        for i in range(len(info)):
            info[i].destroy()
        admin_login(root)
    
    row = tk.Frame(root, bg=bg_color)
    lab = tk.Label(row, width=27, text="Customer Login", font="Aileron 40", anchor='n', fg="chocolate", bg=bg_color)
    row.pack(side=tk.TOP, fill="both",padx=5, pady=20)
    lab.pack(anchor=tk.CENTER)

    row1 = tk.Frame(root,bg=bg_color)
    lab1 = tk.Label(row1, width=20, text="Email", font="Times 20", anchor='w',bg=bg_color)
    ent1 = tk.Entry(row1, font="Times 20")
    row1.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab1.pack(side=tk.LEFT)
    ent1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    row2 = tk.Frame(root,bg=bg_color)
    lab2 = tk.Label(row2, width=20, text="Password", font="Times 20", anchor='w',bg=bg_color)
    ent2 = tk.Entry(row2, font="Times 20",show="*")
    row2.pack(side=tk.TOP, fill=tk.X,padx=5, pady=10)
    lab2.pack(side=tk.LEFT)
    ent2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    button_row1 = tk.Frame(root, bg=bg_color)
    button1 = tk.Button(button_row1, text="Login", font="Times 20", command=login)
    button_row1.pack(side=tk.TOP, fill=tk.X, padx=100, pady=25)
    button1.pack(anchor='n')

    row3 = tk.Frame(root,bg=bg_color)
    lab3 = tk.Label(row3, width=20, text="Don't have an account", font="Times 20", anchor='w',bg=bg_color)
    button3 = tk.Button(row3, text="Sign up", font="Times 20", command=signup)
    row3.pack(side=tk.TOP, fill=tk.X,padx=5, pady=50)
    lab3.pack(side=tk.LEFT)
    button3.pack(side=tk.LEFT)

    button_row2 = tk.Frame(root, bg=bg_color)
    button4 = tk.Button(button_row2, text="Employee", font="Times 20", command=employee)
    button5 = tk.Button(button_row2, text="Admin", font="Times 20", command=admin)
    button_row2.pack(side=tk.TOP, fill=tk.X, padx=100, pady=25)
    button4.pack(side=tk.LEFT)
    button5.pack(side=tk.RIGHT)
    
    root.mainloop()
    return


customer_login(root)


