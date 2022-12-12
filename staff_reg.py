import re
from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkinter import ttk

def insert():
    get_username = e_username.get()
    get_name = e_name.get()
    get_branch=e_branch.get()
    get_phone = e_phone.get()
    get_pwd=e_pwd.get()
    get_repwd=e_repwd.get()

    if get_username == "" or get_name == "" or get_phone=="" or get_branch=="" or get_pwd=="" or get_repwd=="":
        MessageBox.showerror("Insert Status", "All fields are required")
    else:
       if get_pwd != get_repwd:
            MessageBox.showerror("Password Error", "Confirm Password should be same")
       else:
         if not re.match("(?=.*\d).{10}",get_phone):
             MessageBox.showerror("Mobile Number Error", "Please enter the valid mobile number")
         else:
           try:
            con = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor = con.cursor()
            cursor.execute("Insert into staff_login values('" + get_username + "','" + get_name + "','" + get_branch + "','" + get_phone + "','" + get_pwd + "')")
            cursor.execute("commit")
            e_username.delete(0, 'end')
            e_name.delete(0, 'end')
            e_phone.delete(0, 'end')
            e_branch.set('')
            e_pwd.delete(0, 'end')
            e_repwd.delete(0, 'end')
            MessageBox.showinfo("Registration Status", "Account Created Successfully")
            con.close()
           except Exception as e:
            MessageBox.showerror("Backend Error", e)

def gotoLogin1(self):
    root.destroy()
    import staff_login

root = Tk()
pw = ttk.PanedWindow(root, orient=HORIZONTAL)
pw.pack(fill=BOTH, expand=True)
frame1 = Frame(pw, relief=SUNKEN, bg="#4169E1")
frame2 = Frame(pw, relief=SUNKEN, bg="#fff")
pw.add(frame1, weight=2)
pw.add(frame2, weight=4)
root.geometry("600x500")
root.title("Staff Registration")
root.iconbitmap("al_icon.ico")

img = PhotoImage(file="avater.png")
label = Label(frame1, image=img, bg="#4169E1")
label.place(x=20, y=100)

reglb = Label(frame1, text="Staff \nRegistration", font="Verdana 15 bold", bg="#4169E1")
reglb.place(x=20, y=255)

img2 = PhotoImage(file="VIT2.png")
label = Label(frame2, image=img2, bg="#fff")
label.place(x=80,y=10)

username = Label(frame2, text="Username", font="Verdana 11", bg="#fff")
username.place(x=20, y=120)

name = Label(frame2, text="Name", font="Verdana 11",bg="#fff")
name.place(x=20, y=160)

branch = Label(frame2, text="Branch", font="Verdana 11", bg="#fff")
branch.place(x=20, y=200)

phone = Label(frame2, text="Mobile No", font="Verdana 11", bg="#fff")
phone.place(x=20, y=240)

pwd = Label(frame2, text="Password", font="Verdana 11", bg="#fff")
pwd.place(x=20, y=280)

repwd = Label(frame2, text="Retype Password", font="Verdana 11", bg="#fff")
repwd.place(x=20, y=320)

e_username = ttk.Entry(frame2)
e_username.place(x=180, y=120)

e_name = ttk.Entry(frame2)
e_name.place(x=180, y=160)

e_branch = ttk.Combobox(frame2, width=17, state="readonly")
e_branch['values'] = ('Information Technology', 'Computer Engineering', 'Electronics Engineering', 'Electronics and Telecommunication Engineering', 'Biomedical Engineering', 'Management Studies')
e_branch.place(x=180,y=200)

e_phone = ttk.Entry(frame2)
e_phone.place(x=180, y=240)

e_pwd=ttk.Entry(frame2,show="*")
e_pwd.place(x=180,y=280)

e_repwd=ttk.Entry(frame2,show="*")
e_repwd.place(x=180,y=320)

insert = Button(frame2, text="  Register  ", bg="blue", fg="white", font="Verdana 12 bold", command=insert)
insert.place(x=130, y=380)

gotoLogin = Label(frame2, text="Already have an account ? Click here to Login", font="Verdana 11", bg="#fff")
gotoLogin.place(x=20, y=430)
gotoLogin.bind("<Button-1>",gotoLogin1)

root.mainloop()