# This is a store management software

# I used tkinter to implement GUI and MySQL as a database
# I focused mainly on the backend logic and used simple GUI buttons to navigate this software

# Features:
# User signup functionality.
# User login functionality.
# Ability to add item details (name, quantity, price, shelf number) to the database.
# Item search functionality.
# Add items to cart.
# Cart checkout.
# Automatic database update after each sale.

# Concepts used:
# 1) Functions and methods.
# 2) MySQL Database connection through python.
# 3) Different MySQL queries.
# 4) Dictionary to show cart details.
# 5) Loops and conditional statements.
# 6) Object oriented programming.
# 7) Different levels of scope.


import mysql.connector
from tkinter import *

class store:
    def __init__(self,name,price,quantity,shelf_num):
        self.item_name = name
        self.item_price = price
        self.item_quantity = quantity
        self.item_shelf_num = shelf_num

    # Adds details to database
    def set_details(self):
        # Adds details to database
        # Need to append these details to database
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
        mycursor = mydb.cursor()
        mycursor.execute(f"insert into {item_info} values('{self.item_name}','{self.item_price}','{self.item_quantity}','{self.item_shelf_num}');")
        mydb.commit()
        mycursor.close()
        print('details uploaded to database')

    # Retrieves details from database
    def get_details(self,search_item):
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
        mycursor = mydb.cursor()
        self.search_item = search_item
        mycursor.execute(f"select * from {item_info} where item_name ='{self.search_item}';")
        for i in mycursor:
            global i_name
            i_name = i[0]
            global i_price
            i_price = i[1]
            global i_quantity
            i_quantity = i[2]
            global i_shelf
            i_shelf = i[3]
            print(i[0], i[1], i[2],i[3])
            s_item_to_s_details()
        mycursor.close()

# GUI fuction
def firstpage_gui():
    global main_window
    main_window = Tk()
    Label(main_window, text='Store management software').grid(row=0, column=0)
    Button(main_window, text='Signup', command=firstpage_to_signup).grid(row=1, column=0)
    Button(main_window, text='Login', command=firstpage_to_login).grid(row=2, column=0)
    main_window.mainloop()

# This is a transition fuction
# This fuction destroys the previous window and calls the next function
# Mainly i used this to reuse the gui windows multiple times
def firstpage_to_signup():
    main_window.destroy()
    signup_gui()


# Transition fuction
def firstpage_to_login():
    main_window.destroy()
    login_gui()



def signup_gui():
    global signup_window
    signup_window = Tk()
    Label(signup_window, text='Signup').grid(row=0, column=0)
    Label(signup_window, text='Enter username:').grid(row=1, column=0)
    Label(signup_window, text='Enter password:').grid(row=2, column=0)
    global username
    username = Entry(signup_window, width=50, borderwidth=3)
    username.grid(row=1, column=1,sticky=W)
    global password
    password = Entry(signup_window, width=50, borderwidth=3)
    password.grid(row=2, column=1,sticky=W)
    Button(signup_window, text='Signup', command=signup).grid(row=3, column=1)
    signup_window.mainloop()

# Adds the signup details to database
def signup():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    signup = username.get()
    item_info = username.get()+'2'
    mycursor.execute(f'CREATE TABLE {signup} (username varchar(20) not null, password varchar(20),primary key(username));')
    mycursor.execute(f"insert into {signup} values('{username.get()}','{password.get()}');")
    mycursor.execute(f'CREATE TABLE {item_info} (item_name varchar(20) not null, price int, quantity_available int, shelf_number varchar(20),primary key(item_name));')
    mycursor.close()
    signup_window.destroy()
    print('signed up')
    firstpage_gui()

def login_gui():
    global login_window
    login_window = Tk()
    Label(login_window, text='Login').grid(row=0, column=0)
    Label(login_window, text='Enter username:').grid(row=1, column=0)
    Label(login_window, text='Enter password:').grid(row=2, column=0)

    global Username
    Username = Entry(login_window, width=50, borderwidth=3)
    Username.grid(row=1, column=1)
    global Password
    Password = Entry(login_window, width=50, borderwidth=3)
    Password.grid(row=2, column=1)

    Button(login_window, text='Login', command=login).grid(row=3, column=1)
    login_window.mainloop()

# Checks if signup details match with login details
# If matches goes to the next page
def login():
    global item_info
    item_info = Username.get() + '2'
    global signup
    signup = Username.get()
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute(f"select * from {signup} where username='{Username.get()}';")
    for i in mycursor:
        if i[0] == f'{Username.get()}' and i[1] == f'{Password.get()}':
            mycursor.close()
            login_window.destroy()
            cart_refresh()
            print('logged in')
    else:
        mycursor.close()
        login_window.destroy()
        print('enter correct login details')
        login_gui()


# Deletes old cart table and creates new cart table
def cart_refresh():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute("show tables;")
    for i in mycursor:
        l = list(i)
        if l[0] == 'cart':
            cart_delete()
            cart_create()
            print('cart found')
            afterlogin_gui()
            break
    else:
        print('cart not found')
        cart_create()
        afterlogin_gui()

    mycursor.close()

# User can add items here
# User can search item details here
def afterlogin_gui():
    global afterlogin_window
    afterlogin_window = Tk()
    Label(afterlogin_window, text='Welcome user').grid(row=0, column=0)
    Button(afterlogin_window, text='Add item', command=afterlogin_to_additem_db).grid(row=1, column=0)
    Button(afterlogin_window, text='Search item', command=afterlogin_to_searchitem).grid(row=2, column=0)
    afterlogin_window.mainloop()

def afterlogin_to_additem_db():
    afterlogin_window.destroy()
    additem_gui()

def afterlogin_to_searchitem():
    afterlogin_window.destroy()
    searchitem_gui()

# When user adds details here, object is created and items are added to database
def additem_gui():
    global additem_window
    additem_window = Tk()
    Label(additem_window, text='Add item details here').grid(row=0, column=0)
    Label(additem_window, text='Item name').grid(row=1, column=0)
    global item_name
    item_name = Entry(additem_window, width=50, borderwidth=3)
    item_name.grid(row=1, column=1,sticky=W)
    Label(additem_window, text='Price').grid(row=2, column=0)
    global item_price
    item_price = Entry(additem_window, width=50, borderwidth=3)
    item_price.grid(row=2, column=1,sticky=W)
    Label(additem_window, text='Quantity adding').grid(row=3, column=0)
    global item_quantity
    item_quantity = Entry(additem_window, width=50, borderwidth=3)
    item_quantity.grid(row=3, column=1,sticky=W)
    Label(additem_window, text='Shelf number').grid(row=4, column=0)
    global item_shelf_num
    item_shelf_num = Entry(additem_window, width=50, borderwidth=3)
    item_shelf_num.grid(row=4, column=1,sticky=W)
    Button(additem_window, text='Add item', command=add_item).grid(row=5, column=1)
    Button(additem_window, text='back', command=additem_gui_to_afterlogin).grid(row=5, column=0)
    additem_window.mainloop()

def add_item():
    global obj
    obj = store(item_name.get(), item_price.get(), item_quantity.get(), item_shelf_num.get())
    obj.set_details()
    additem_window.destroy()
    additem_gui()

def additem_gui_to_afterlogin():
    additem_window.destroy()
    afterlogin_gui()


def searchitem_gui():
    global searchitem_window
    searchitem_window = Tk()
    Label(searchitem_window, text='Search item details here').grid(row=0, column=0)
    Label(searchitem_window, text='Item name').grid(row=1, column=0)
    global search_item
    search_item = Entry(searchitem_window, width=50, borderwidth=3)
    search_item.grid(row=1, column=1,sticky=W)
    Button(searchitem_window, text='Search', command=searchitem_to_searchdetails).grid(row=5, column=1)
    searchitem_window.mainloop()

# User can search details of added items such as item quantity available, shelf number and its price
def searchitem_to_searchdetails():
    globals()['obj'].get_details(search_item.get())
    print('get details called')

def s_item_to_s_details():
    searchitem_window.destroy()
    searchdetails_gui()


def searchdetails_gui():
    global searchdetails_window
    searchdetails_window = Tk()
    Label(searchdetails_window, text='Search details').grid(row=0, column=0)
    Label(searchdetails_window, text='Item name:').grid(row=1, column=0)
    Label(searchdetails_window, text= i_name).grid(row=1, column=1)
    Label(searchdetails_window, text='Price:').grid(row=2, column=0)
    Label(searchdetails_window, text= i_price).grid(row=2, column=1)
    Label(searchdetails_window, text='Quantity:').grid(row=3, column=0)
    Label(searchdetails_window, text= i_quantity).grid(row=3, column=1)
    Label(searchdetails_window, text='Shelf number:').grid(row=4, column=0)
    Label(searchdetails_window, text= i_shelf).grid(row=4, column=1)
    Button(searchdetails_window, text='Add to cart', command=addtocart).grid(row=5, column=1)
    Button(searchdetails_window, text='Add another item', command=searchdetails_to_searchitem_gui).grid(row=6, column=1)
    Button(searchdetails_window, text='Go to cart', command=searchdetails_to_cart).grid(row=7, column=1)
    searchdetails_window.mainloop()

def cart_create():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE cart (item_name varchar(20), quantity int, price int);")
    mydb.commit()
    mycursor.close()

def addtocart():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("show tables;")
    for i in mycursor:
        l = list(i)
        if l[0] == 'cart':
            print('cart found')
            break
    else:
        print('cart not found')
        cart_create()

    mycursor.execute(f"insert into cart values('{i_name}',1,{i_price});")
    mydb.commit()
    mycursor.close()
    print('item added to cart')

def searchdetails_to_searchitem_gui():
    searchdetails_window.destroy()
    searchitem_gui()

def searchdetails_to_cart():
    searchdetails_window.destroy()
    cart_gui()


# I implemented dictionary to show values
def cart_gui():
    global cart_window
    cart_window = Tk()
    Label(cart_window, text='Cart').grid(row=0, column=0)
    Label(cart_window, text='ITEM NAME').grid(row=1, column=0)
    Label(cart_window, text='QUANTITY').grid(row=1, column=1)
    Label(cart_window, text='PRICE').grid(row=1, column=2)
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute("select * from cart;")
    global dict
    dict = {}
    for i in mycursor:
        dict[mycursor.rowcount] = i
    for i in range(1,len(dict)+1):
        for j in range(len(dict[i])):
            Label(cart_window, text=dict[i][j]).grid(row=i+2, column=j)

    Label(cart_window, text='TOTAL:').grid(row=mycursor.rowcount+3, column=2)

    total = 0
    for i in range(1,len(dict)+1):
        total = total + dict[i][2]

    Label(cart_window, text=total).grid(row=mycursor.rowcount+3, column=3)
    b = Button(cart_window, text='Checkout',command=cart_to_receipt)
    b.grid(row=mycursor.rowcount+4, column=2,sticky=W)
    mycursor.close()
    cart_window.mainloop()

def cart_to_receipt():
    cart_window.destroy()
    update_table()
    receipt_gui()

# This updates the quantity available in the item_info table after checkout
def update_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT item_name, quantity FROM cart;")

    dict1 = {}
    for i in mycursor:
        dict1[mycursor.rowcount] = i

    dict2 = {}
    mycursor.execute(f"SELECT item_name, quantity_available FROM {item_info};")
    for i in mycursor:
        dict2[mycursor.rowcount] = i

    print(dict1)
    print(dict2)
    mycursor.close()

    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    quantity = 0
    for i in range(1, len(dict2) + 1):
        for j in range(1, len(dict1) + 1):
            if dict2[i][0] == dict1[j][0]:
                quantity = dict2[i][1] - dict1[j][1]
                print(quantity)
                mycursor.execute(f"update {item_info} set quantity_available='{quantity}' where item_name='{dict1[j][0]}';")
    mydb.commit()
    mycursor.close()

def receipt_gui():
    global receipt_window
    receipt_window = Tk()
    Label(receipt_window, text='Receipt').grid(row=0, column=0)
    Label(receipt_window, text='ITEM NAME').grid(row=1, column=0)
    Label(receipt_window, text='QUANTITY').grid(row=1, column=1)
    Label(receipt_window, text='PRICE').grid(row=1, column=2)
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute("select * from cart;")
    dict = {}
    for i in mycursor:
        dict[mycursor.rowcount] = i
    for i in range(1, len(dict) + 1):
        for j in range(len(dict[i])):
            Label(receipt_window, text=dict[i][j]).grid(row=i + 2, column=j)

    Label(receipt_window, text='TOTAL:').grid(row=mycursor.rowcount + 3, column=2)
    total = 0
    for i in range(1, len(dict) + 1):
        total = total + dict[i][2]
    Label(receipt_window, text=total).grid(row=mycursor.rowcount + 3, column=3)
    Button(receipt_window, text='Done',command=receipt_to_searchitem).grid(row=mycursor.rowcount + 4, column=2)
    mycursor.close()
    receipt_window.mainloop()

def receipt_to_searchitem():
    receipt_window.destroy()
    searchitem_gui()
    cart_delete()

def cart_delete():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='Stan@6123', database='abhishek')
    mycursor = mydb.cursor()
    mycursor.execute("drop table cart;")
    mydb.commit()
    mycursor.close()

# Starting point of execution
def main():
    firstpage_gui()

if __name__ == '__main__':
    main()
