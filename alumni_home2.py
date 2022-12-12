import io
import os
from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkinter import ttk, filedialog

from PIL import ImageTk,Image
from sqlalchemy import create_engine

root = Tk()
pw = ttk.PanedWindow(root, orient=VERTICAL)
pw.pack(fill=BOTH, expand=True)
frame1 = Frame(pw, relief=SUNKEN, bg="#4169E1")
frame2 = Frame(pw, relief=SUNKEN, bg="#fff")
pw.add(frame1, weight=1)
pw.add(frame2, weight=6)
root.geometry("920x690")
root.title("VIT Alumni Directory | Alumni Homepage")
root.iconbitmap("al_icon.ico")

def logout():
    root.destroy()
    os.system("alumni_login.py")

#Frame1
label = Label(frame1, text="", bg="#4169E1",fg="#fff", font=('Roboto','15','bold'))
label.place(x=10, y=30)

with open('uname_a.txt', 'r') as f:
    a=f.read()
label.config(text="Welcome "+a)

label2 = Label(frame1, text="Welcome to Alumni Directory Alumni Panel", bg="#4169E1",fg="#fff", font=('Roboto','14','bold'))
label2.place(x=300, y=30)

lg = Button(frame1, text="  Logout  ", bg="blue", fg="white", font=('Roboto','15','bold'), command=logout)
lg.place(x=800, y=25)

#Frame2
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Roboto','13','bold'))
tabControl = ttk.Notebook(frame2)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text='  My Profile  ')
tabControl.add(tab2, text='  Alumni Report  ')
tabControl.add(tab3, text='  Events  ')
tabControl.add(tab4, text='  Jobs  ')
tabControl.add(tab5, text='  Gallery  ')
tabControl.pack(expand=1, fill="both")

bg = PhotoImage(file="backg.png")

# Tab 1
canvas1 = Canvas(tab1, width=600,height=690)
canvas1.pack(fill="both", expand=True)
# Display image
canvas1.create_image(0, 0, image=bg,anchor="nw")
def update():
    global img, filename
    get_rollno = e_rollno.get()
    get_name = e_name.get()
    get_pass=e_pass.get()
    get_phone = e_phone.get()
    get_current=e_current.get()

    if get_rollno == "" or get_name == "" or get_phone == "" or get_pass == "" or get_current == "":
        MessageBox.showerror("Update Status", "All fields are required")
    else:
        try:
            fob = open(filename, 'rb')  # filename from upload_file()
            fob = fob.read()
            data = (get_name,fob,get_pass,get_phone,get_current,get_rollno)  # tuple with data
            my_conn = create_engine("mysql+mysqldb://root:@localhost/vit_alumni_directory")
            my_conn.execute("UPDATE alumni_login set Name=%s,DP=%s,PassoutYear=%s,MobileNo=%s,Study_Work=%s WHERE RollNo=%s",data)
            my_conn.execute("commit")

            e_rollno.delete(0, 'end')
            e_name.delete(0, 'end')
            e_phone.delete(0, 'end')
            e_pass.set('')
            e_current.delete(0, 'end')
            b2.config(text="Image Uploaded", image='', bg="white")
            MessageBox.showinfo("Update Status", "Account Updated Successfully")
            alumni_report()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

def upload_file(): # Image upload and display
    global filename,img
    f_types =[('Png files','*.png'),('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    global b2
    b2 = Label(tab1,image=img) # using Button
    b2.place(x=435, y=320)#display uploaded photo

canvas1.create_text(300, 30, text="RollNo", font=('Roboto','13','bold'))
canvas1.create_text(300, 80, text="Name", font=('Roboto','13','bold'))
canvas1.create_text(300, 130, text="Passout Year", font=('Roboto','13','bold'))
canvas1.create_text(300, 180, text="Phone", font=('Roboto','13','bold'))
canvas1.create_text(300, 230, text="Current Company/College Name", font=('Roboto','13','bold'))
canvas1.create_text(300, 280, text="Update DP", font=('Roboto','13','bold'))

e_rollno=ttk.Entry(tab1, font=('Roboto','13'))
e_rollno.place(x=435,y=20)
e_rollno.insert(0, a)
e_rollno.config(state="readonly")
e_name = ttk.Entry(tab1, font=('Roboto','13'))
e_name.place(x=435,y=70)
e_pass = ttk.Combobox(tab1, width=18, state="readonly", font=('Roboto','13'))
e_pass['values'] = (
       '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
       '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024')
e_pass.place(x=435,y=120)
e_phone = ttk.Entry(tab1, font=('Roboto','13'))
e_phone.place(x=435,y=170)
e_current = ttk.Entry(tab1, font=('Roboto','13'))
e_current.place(x=435,y=220)

uploaddp = Button(tab1, text="  Upload file  ", bg="blue", fg="white", font=('Roboto','13','bold'), command = lambda:upload_file())
uploaddp.place(x=435,y=270)

Button(tab1, text="  Update  ", bg="blue", fg="white", font=('Roboto','13','bold'),command= lambda:update()).place(x=430,y=480)

#Tab2
canvas2 = Canvas(tab2, width=600,height=690)
canvas2.pack(fill="both", expand=True)
# Display image
canvas2.create_image(0, 0, image=bg,anchor="nw")

def filterSearch(*args):
    items = tree3.get_children()
    search1 = q.get().capitalize()
    for i in items:
        if search1 in tree3.item(i)['values'][1]:
            search_var = tree3.item(i)['values']
            tree3.delete(i)
            tree3.insert("", 0, values=search_var)


canvas2.create_text(300, 24, text="Search Alumni", font=('Roboto','13','bold'))
q=StringVar()
search = ttk.Entry(tab2, font=('Roboto','13'),textvariable=q)
search.place(x=410, y=12)
q.trace("w",filterSearch)

try:
  connect1=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
  cursor1=connect1.cursor()
  cursor1.execute("SELECT * FROM alumni_login")

  def alumni_report():
      global tree3
      tree3 = ttk.Treeview(tab2, style = 'style1.Treeview')
      style1 = ttk.Style(tab2)
      style1.configure("style1.Treeview", rowheight=50)  # set row height
      tree3['columns'] = ("RollNo","Name","PassoutYear","MobileNo","Branch","Work Company")
      tree3.column("#0", width=150, stretch='NO',minwidth=150)  # set width
      tree3.column("RollNo", width=100, anchor='w',minwidth=100)
      tree3.column("Name", width=100, anchor='w',minwidth=100)
      tree3.column("PassoutYear", width=100, anchor='w',minwidth=100)
      tree3.column("MobileNo", width=100, anchor='w',minwidth=100)
      tree3.column("Branch", width=150, anchor='w',minwidth=150)
      tree3.column("Work Company", width=150, anchor='w',minwidth=150)

      tree3.heading("#0", anchor='w', text='Image')
      tree3.heading("RollNo", anchor='w', text="RollNo")
      tree3.heading("Name", anchor='w', text="Name")
      tree3.heading("PassoutYear", anchor='w', text="PassoutYear")
      tree3.heading("MobileNo", anchor='w', text="MobileNo")
      tree3.heading("Branch", anchor='w', text="Branch")
      tree3.heading("Work Company", anchor='w', text="Work Company")

      count = 0

      tree3.imglist = []
      for record in cursor1:
          dp = Image.open(io.BytesIO(record[2]))
          dp.thumbnail((50, 50))  # resize the image to desired size
          dp = ImageTk.PhotoImage(dp)
          tree3.insert(parent="", index="end", id=count,
                         image=dp, values=(record[0],record[1],record[3],record[4],record[5],record[6],))  # use "image" option for the image
          tree3.imglist.append(dp)  # save the image reference
          count += 1

      for record in cursor1:
          # print(record)
          tree3.insert(parent='', index='end', id=count, text='Parent',
                         values=(record[0]))
          count += 1
      tree3.place(x=40, y=50)

except Exception as e:
    MessageBox.showerror("Backend Error", e)
alumni_report()

#Tab3
canvas3 = Canvas(tab3, width=600,height=690)
canvas3.pack(fill="both", expand=True)
# Display image
canvas3.create_image(0, 0, image=bg,anchor="nw")
try:
    connect2=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor2=connect2.cursor()
    cursor2.execute("SELECT * FROM events")

    tree=ttk.Treeview(tab3)
    tree['show'] = 'headings'
    tree["columns"]=("SrNo","EventName","Description","Date","Time","Venue")
    tree.column("SrNo",width=50,minwidth=50)
    tree.column("EventName",width=190,minwidth=190)
    tree.column("Description", width=200, minwidth=200)
    tree.column("Date",width=100,minwidth=100)
    tree.column("Time",width=80,minwidth=80)
    tree.column("Venue",width=150,minwidth=150)

    #assign headings
    tree.heading("SrNo",text="SrNo")
    tree.heading("EventName",text="EventName")
    tree.heading("Description", text="Description")
    tree.heading("Date",text="Date")
    tree.heading("Time",text="Time")
    tree.heading("Venue",text="Venue")

    i=0
    for ro in cursor2:
        tree.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5]))
        i=i+1
    tree.place(x=75,y=20)
except Exception as e:
    MessageBox.showerror("Backend Error", e)

#Tab 4
canvas4 = Canvas(tab4, width=600,height=690)
canvas4.pack(fill="both", expand=True)
# Display image
canvas4.create_image(0, 0, image=bg,anchor="nw")
def jobpost():
    get_company = e_company.get()
    get_post = e_post.get()
    get_minquali = e_minquali.get()
    get_location = e_location.get()
    get_applylink = e_applylink.get()

    if get_company == "" or get_post == "" or get_minquali == "" or get_location == "" or get_applylink == "":
        MessageBox.showerror("Insert Status", "All fields are required")
    else:
        try:
            connect4 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor4 = connect4.cursor()
            cursor4.execute("Insert into jobs (Company,Post,MinQuali,Location,ApplyLink) values ('" + get_company + "','" + get_post + "','" + get_minquali + "','" + get_location + "','" + get_applylink + "')")
            cursor4.execute("commit")

            e_company.delete(0, 'end')
            e_post.delete(0, 'end')
            e_location.delete(0, 'end')
            e_applylink.delete(0, 'end')
            MessageBox.showinfo("Post Status", "Job Posted")
            connect4.close()
            showjobs()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

canvas4.create_text(300, 30, text="Company", font=('Roboto','13','bold'))
canvas4.create_text(300, 80, text="Post", font=('Roboto','13','bold'))
canvas4.create_text(300, 130, text="Min Qualification", font=('Roboto','13','bold'))
canvas4.create_text(300, 180, text="Location", font=('Roboto','13','bold'))
canvas4.create_text(300, 230, text="Apply Link", font=('Roboto','13','bold'))

e_company = ttk.Entry(tab4, width=20, font=('Roboto','13'))
e_company.place(x=435,y=20)

e_post = ttk.Entry(tab4, width=20, font=('Roboto','13'))
e_post.place(x=435,y=70)

e_minquali = ttk.Combobox(tab4, width=18, state="readonly", font=('Roboto','13'))
e_minquali['values'] = (
'BE/BTech(IT/CO)', 'ME/MTech(IT/CO)', 'BE/BTech(EXTC/ETRX)', 'ME/MTech(EXTC/ETRX)', 'BE/BTech(BIOM)', 'ME/MTech(BIOM)')
e_minquali.place(x=435,y=120)

e_location = ttk.Entry(tab4, width=20, font=('Roboto','13'))
e_location.place(x=435,y=170)

e_applylink = ttk.Entry(tab4, width=20, font=('Roboto','13'))
e_applylink.place(x=435,y=220)

post = Button(tab4, text="  Post  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=jobpost)
post.place(x=435,y=255)
def showjobs():
  try:
    connect3=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor3=connect3.cursor()
    cursor3.execute("SELECT * FROM jobs")

    tree2=ttk.Treeview(tab4)
    tree2['show'] = 'headings'
    tree2["columns"]=("ID","Company","Post","MinQuali","Location","ApplyLink")
    tree2.column("ID", width=50, minwidth=50)
    tree2.column("Company",width=100,minwidth=100)
    tree2.column("Post",width=150,minwidth=150)
    tree2.column("MinQuali",width=150,minwidth=150)
    tree2.column("Location",width=100,minwidth=100)
    tree2.column("ApplyLink",width=250,minwidth=250)

    #assign headings
    tree2.heading("ID", text="ID")
    tree2.heading("Company",text="Company")
    tree2.heading("Post",text="Post")
    tree2.heading("MinQuali",text="MinQuali")
    tree2.heading("Location",text="Location")
    tree2.heading("ApplyLink",text="ApplyLink")

    i=0
    for ro in cursor3:
        tree2.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5]))
        i=i+1
    tree2.place(x=80,y=300)

  except Exception as e:
    MessageBox.showerror("Backend Error", e)
showjobs()

#Tab 5
canvas5 = Canvas(tab5, width=600,height=690)
canvas5.pack(fill="both", expand=True)
# Display image
canvas5.create_image(0, 0, image=bg,anchor="nw")
img = PhotoImage(file="1.png")
img2 =PhotoImage(file="2.png")
img3 =PhotoImage(file="3.png")
l = Label(tab5)
l.place(x=65,y=65)
x = 1
def move():
    global x
    if x == 4:
        x = 1
    if x == 1:
        l.config(image=img)
    elif x == 2:
        l.config(image=img2)
    elif x == 3:
        l.config(image=img3)
    x = x + 1
    tab5.after(2000, move)

move()

root.mainloop()