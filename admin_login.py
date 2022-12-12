from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkinter import ttk

def login():
    get_username = e_username.get()
    get_pwd=e_pwd.get()
    with open('uname_ad.txt', 'w') as f:
        f.write(get_username)

    if get_username == "" or get_pwd == "":
        MessageBox.showerror("Login Error", "All fields are required")
    else:
        try:
            con = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor=con.cursor()

            sql = "select * from admin_login where Username=%s and Password=%s"
            cursor.execute(sql, [(get_username), (get_pwd)])
            results=cursor.fetchall()
            if results:
                MessageBox.showinfo("Login Success", "Welcome "+get_username)
                root.destroy()
                import admin_home
            else:
                MessageBox.showerror("Login Error", "Username/Password is not valid")
                return False
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

def gotoReg1(self):
    root.destroy()
    import admin_reg

def switch_u(self):
    root.destroy()
    import welcome

root = Tk()
pw = ttk.PanedWindow(root, orient=HORIZONTAL)
pw.pack(fill=BOTH, expand=True)
frame1 = Frame(pw, relief=SUNKEN, bg="#4169E1")
frame2 = Frame(pw, relief=SUNKEN, bg="#fff")
pw.add(frame1, weight=2)
pw.add(frame2, weight=4)
root.geometry("600x500")
root.title("Admin Login")
root.iconbitmap("al_icon.ico")

img = PhotoImage(file="avater.png")
label = Label(frame1, image=img, bg="#4169E1")
label.place(x=20, y=100)

reglb = Label(frame1, text="Admin Login", font="Verdana 15 bold", bg="#4169E1")
reglb.place(x=25, y=255)

img2 = PhotoImage(file="VIT2.png")
label = Label(frame2, image=img2, bg="#fff")
label.place(x=80,y=10)

tit = Label(frame2, text="Alumni Directory", font="Verdana 15", bg="#fff")
tit.place(x=100, y=120)

username = Label(frame2, text="Username", font="Verdana 11", bg="#fff")
username.place(x=20, y=180)

pwd = Label(frame2, text="Password", font="Verdana 11",bg="#fff")
pwd.place(x=20, y=230)

e_username = ttk.Entry(frame2)
e_username.place(x=180, y=180)

e_pwd = ttk.Entry(frame2,show="*")
e_pwd.place(x=180, y=230)

login = Button(frame2, text="  Login  ", bg="blue", fg="white", font="Verdana 12 bold", command=login)
login.place(x=130, y=280)

gotoReg = Label(frame2, text="Don't have an account ? Click here to Register", font="Verdana 11", bg="#fff")
gotoReg.place(x=20, y=330)
gotoReg.bind("<Button-1>",gotoReg1)

switch_user = Label(frame2, text="Switch User", font="Verdana 11", bg="#fff")
switch_user.place(x=275, y=370)
switch_user.bind("<Button-1>",switch_u)

root.mainloop()