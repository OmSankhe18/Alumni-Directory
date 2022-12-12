import re
from tkinter import *
import tkinter.messagebox as MessageBox
from tkinter import ttk, filedialog
from sqlalchemy import create_engine
from PIL import ImageTk

def insert():
    global img, filename
    get_rollno = e_rollno.get()
    get_name = e_name.get()
    get_passout=e_pass.get()
    get_phone = e_phone.get()
    get_branch=e_branch.get()
    get_pwd=e_pwd.get()
    get_repwd=e_repwd.get()

    if get_rollno == "" or get_name == "" or get_passout == "" or get_phone=="" or get_branch=="" or get_pwd=="" or get_repwd=="":
        MessageBox.showerror("Insert Status", "All fields are required")
    else:
        if get_pwd!=get_repwd:
            MessageBox.showerror("Password Error", "Confirm Password should be same")
        else:
          if not re.match("(?=.*\d).{10}",get_phone):
              MessageBox.showerror("Mobile Number Error", "Please enter the valid mobile number")
          else:
            try:
                conn = create_engine("mysql+mysqldb://root:@localhost/vit_alumni_directory")

                sql = "select * from passout where RollNo=%s and Branch=%s and PassoutYear=%s"
                data=conn.execute(sql, [(get_rollno), (get_branch), (get_passout)])
                results = data.fetchall()
                if results:
                    fob = open(filename, 'rb')  # filename from upload_file()
                    fob = fob.read()
                    studywork="Not Updated"
                    data = (get_rollno, get_name,fob,get_passout, get_phone, get_branch, studywork, get_pwd)  # tuple with data
                    conn.execute("INSERT INTO  alumni_login (RollNo,Name,DP,PassoutYear,MobileNo,Branch,Study_Work,Password) \
                                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", data)
                    conn.execute("commit")

                    e_rollno.delete(0, 'end')
                    e_name.delete(0, 'end')
                    e_phone.delete(0, 'end')
                    e_pass.set('')
                    e_branch.set('')
                    e_pwd.delete(0, 'end')
                    e_repwd.delete(0, 'end')
                    b2.config(text="Image Uploaded",image='', bg="white")
                    MessageBox.showinfo("Success", "Registration Successful")
                    return True
                else:
                    MessageBox.showerror("Error", "Registration Failed")
                    return False
            except Exception as e:
                MessageBox.showerror("Backend Error",e)

def gotoLogin1(self):
    root.destroy()
    import alumni_login

root = Tk()
pw = ttk.PanedWindow(root, orient=HORIZONTAL)
pw.pack(fill=BOTH, expand=True)
frame1 = Frame(pw, relief=SUNKEN, bg="#4169E1")
frame2 = Frame(pw, relief=SUNKEN, bg="#fff")
pw.add(frame1, weight=2)
pw.add(frame2, weight=5)
root.geometry("700x600")
root.title("Alumni Registration")
root.iconbitmap("al_icon.ico")

img = PhotoImage(file="avater.png")
label = Label(frame1, image=img, bg="#4169E1")
label.place(x=20, y=170)

reglb = Label(frame1, text="Alumni \nRegistration", font="Verdana 15 bold", bg="#4169E1")
reglb.place(x=20, y=325)

img2 =PhotoImage(file="VIT2.png")
label = Label(frame2, image=img2, bg="#fff")
label.place(x=80,y=10)

rollno = Label(frame2, text="RollNo", font="Verdana 11", bg="#fff")
rollno.place(x=20, y=120)

name = Label(frame2, text="Name", font="Verdana 11",bg="#fff")
name.place(x=20, y=160)

passout = Label(frame2, text="Passout Year", font="Verdana 11",bg="#fff")
passout.place(x=20, y=200)

phone = Label(frame2, text="Mobile No", font="Verdana 11", bg="#fff")
phone.place(x=20, y=240)

branch = Label(frame2, text="Branch", font="Verdana 11", bg="#fff")
branch.place(x=20, y=280)

pwd = Label(frame2, text="Password", font="Verdana 11", bg="#fff")
pwd.place(x=20, y=320)

repwd = Label(frame2, text="Retype Password", font="Verdana 11", bg="#fff")
repwd.place(x=20, y=360)

dp= Label (frame2, text="Display Picture", font="Verdana 11", bg="#fff")
dp.place(x=20, y=400)

e_rollno = ttk.Entry(frame2,font="Verdana 11")
e_rollno.place(x=180, y=120)

e_name = ttk.Entry(frame2,font="Verdana 11")
e_name.place(x=180, y=160)

e_pass = ttk.Combobox(frame2, width=18, state="readonly",font="Verdana 11")
e_pass['values'] = ('2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024')
e_pass.place(x=180, y=200)

e_phone = ttk.Entry(frame2,font="Verdana 11")
e_phone.place(x=180, y=240)

e_branch = ttk.Combobox(frame2, width=18, state="readonly",font="Verdana 11")
e_branch['values'] = ('Information Technology', 'Computer Engineering', 'Electronics Engineering', 'Electronics and Telecommunication Engineering', 'Biomedical Engineering', 'Management Studies')
e_branch.place(x=180, y=280)

e_pwd=ttk.Entry(frame2,show="*",font="Verdana 11")
e_pwd.place(x=180, y=320)

e_repwd=ttk.Entry(frame2,show="*",font="Verdana 11")
e_repwd.place(x=180,y=360)

def upload_file(): # Image upload and display
    global filename,imgdp
    f_types =[('Png files','*.png'),('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    imgdp = ImageTk.PhotoImage(file=filename)
    global b2
    b2=Label(frame2,image=imgdp,background="#fff") # using Button
    b2.place(x=300,y=400)#display uploaded photo

uploaddp = Button(frame2, text="  Upload file  ", bg="blue", fg="white", font="Verdana 11", command = lambda:upload_file())
uploaddp.place(x=180,y=400)

insert = Button(frame2, text="  Register  ", bg="blue", fg="white", font="Verdana 12 bold", command=insert)
insert.place(x=130, y=490)

gotoLogin = Label(frame2, text="Already have an account ? Click here to Login", font="Verdana 11", bg="#fff")
gotoLogin.place(x=20, y=560)
gotoLogin.bind("<Button-1>",gotoLogin1)

root.mainloop()