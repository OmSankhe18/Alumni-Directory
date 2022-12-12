import csv
import io
import os
from tkinter import *
import tkinter.messagebox as MessageBox

import mysql.connector as mysql
from PIL import ImageTk,Image
from tkinter import ttk, filedialog
from tkcalendar import DateEntry

root = Tk()
pw = ttk.PanedWindow(root, orient=VERTICAL)
pw.pack(fill=BOTH, expand=True)
frame1 = Frame(pw, relief=SUNKEN, bg="#4169E1")
frame2 = Frame(pw, relief=SUNKEN, bg="#fff")
pw.add(frame1, weight=1)
pw.add(frame2, weight=6)
root.geometry("920x690")
root.title("VIT Alumni Directory | Staff Homepage")
root.iconbitmap("al_icon.ico")

def logout():
    root.destroy()
    import staff_login

#Frame1
label = Label(frame1, text="", bg="#4169E1",fg="#fff", font=('Roboto','15','bold'))
label.place(x=10, y=30)

with open('uname_s.txt', 'r') as f:
    a=f.read()
label.config(text="Welcome "+a)

label2 = Label(frame1, text="Welcome to Alumni Directory Staff Panel", bg="#4169E1",fg="#fff", font=('Roboto','15','bold'))
label2.place(x=280, y=30)

lg = Button(frame1, text="  Logout  ", bg="blue", fg="white", font=('Roboto','15','bold'), command=logout)
lg.place(x=800, y=25)

#Frame2
s = ttk.Style()
s.configure('TNotebook.Tab', font=('URW Gothic L','11','bold') )
tabControl = ttk.Notebook(frame2)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='  Alumni Report  ')
tabControl.add(tab2, text='  Add Database  ')
tabControl.add(tab3, text='  Events  ')
tabControl.add(tab4, text='  Jobs  ')
tabControl.pack(expand=1, fill="both")

#Tab 1
bg = PhotoImage(file="backg.png")
# Tab 1
canvas1 = Canvas(tab1, width=600,height=690)
canvas1.pack(fill="both", expand=True)
# Display image
canvas1.create_image(0, 0, image=bg,anchor="nw")
def filterSearch(*args):
    items=tree3.get_children()
    search1=q.get().capitalize()
    for i in items:
        if search1 in tree3.item(i)['values'][1]:
            search_var=tree3.item(i)['values']
            tree3.delete(i)
            tree3.insert("",0,values=search_var)

canvas1.create_text(300, 24, text="Search Alumni", font=('Roboto','13','bold'))

q=StringVar()
search = ttk.Entry(tab1, font=('Roboto','13','bold'),textvariable=q)
search.place(x=410, y=12)
q.trace("w",filterSearch)

try:
  connect1=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
  cursor1=connect1.cursor()
  cursor1.execute("SELECT * FROM alumni_login")

  def alumni_report():
      global tree3
      tree3 = ttk.Treeview(tab1, style='style1.Treeview')
      style1 = ttk.Style(tab2)
      style1.configure("style1.Treeview", rowheight=50)  # set row height
      tree3['columns'] = ("RollNo", "Name", "PassoutYear", "MobileNo", "Branch", "Work Company")
      tree3.column("#0", width=150, stretch='NO', minwidth=150)  # set width
      tree3.column("RollNo", width=100, anchor='w', minwidth=100)
      tree3.column("Name", width=100, anchor='w', minwidth=100)
      tree3.column("PassoutYear", width=100, anchor='w', minwidth=100)
      tree3.column("MobileNo", width=100, anchor='w', minwidth=100)
      tree3.column("Branch", width=150, anchor='w', minwidth=150)
      tree3.column("Work Company", width=150, anchor='w', minwidth=150)

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
                       image=dp, values=(
              record[0], record[1], record[3], record[4], record[5], record[6],))  # use "image" option for the image
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

al_count = len(tree3.get_children())
al_count_lbl=Label(tab1, text="",  font=('Roboto','13','bold'),bg="white")
al_count_lbl.place(x=50,y=520)
al_count_lbl.config(text="Total Alumni Registered: "+str(al_count))
#tab2
canvas2 = Canvas(tab2, width=600,height=690)
canvas2.pack(fill="both", expand=True)
# Display image
canvas2.create_image(0, 0, image=bg,anchor="nw")
def delp():
    if e_srno.get() == "":
        MessageBox.showerror("Fetch Status", "ID is compulsory for delete")
    else:
        try:
            connect5 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor5 = connect5.cursor()
            cursor5.execute("delete from passout where SrNo='" + e_srno.get() + "'")
            cursor5.execute("commit")
            e_srno.delete(0, 'end')
            e_rollno.delete(0, 'end')
            e_name.delete(0, 'end')
            e_pass.delete(0, 'end')
            e_branchh.delete(0, 'end')
            showdb()
            MessageBox.showinfo("Delete Status", "Deleted Successfully")
            connect5.close()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

def adddb():
    get_srno=e_srno.get()
    get_rollno = e_rollno.get()
    get_name = e_name.get()
    get_pass = e_pass.get()
    get_branchh = e_branchh.get()

    if get_srno == "" or get_rollno == "" or get_name == "" or get_pass == ""  or get_branchh == "":
        MessageBox.showerror("Insert Status", "All fields are required")
    else:
        try:
            connect6 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor6 = connect6.cursor()
            cursor6.execute("Insert into passout values('" + get_srno + "','" + get_rollno + "','" + get_name + "','" + get_branchh + "','" + get_pass + "')")
            cursor6.execute("commit")
            e_srno.delete(0, 'end')
            e_rollno.delete(0, 'end')
            e_name.delete(0, 'end')
            e_pass.set('')
            e_branchh.set('')
            MessageBox.showinfo("Insert Status", "Data Added Successfully")
            connect6.close()
            showdb()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

mydata=[]

def update(rows):
    global mydata
    mydata=rows
    for i in rows:
        tree5.insert('','end',values=i)

def importcsv():
  try:
    fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV", filetypes=(("CSV File","*.csv"),("All Files","*.*")))
    with open(fln) as myfile:
        csvread=csv.reader(myfile,delimiter=",")
        for i in csvread:
            mydata.append(i)
    update(mydata)
  except Exception as e:
      MessageBox.showerror("Error",e)

def savedb():
  try:
    connect7 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
    cursor7 = connect7.cursor()
    if MessageBox.askyesno("Confirmation","Are you sure want to save data to database ?"):
        for i in mydata:
            srno = i[0]
            rollno=i[1]
            name=i[2]
            branch=i[3]
            passout=i[4]
            query="Insert into passout (SrNo,RollNo,Name,Branch,PassoutYear) values (%s,%s,%s,%s,%s)"
            cursor7.execute(query,(srno,rollno,name,branch,passout))
            cursor7.execute("commit")
        MessageBox.showinfo("Data Saved", "Data inserted in Database")
    else:
        return False
  except Exception as e:
      MessageBox.showerror("Error",e)


canvas2.create_text(300, 30, text="SrNo", font=('Roboto','13','bold'))
canvas2.create_text(300, 80, text="Roll No", font=('Roboto','13','bold'))
canvas2.create_text(300, 130, text="Name", font=('Roboto','13','bold'))
canvas2.create_text(300, 180, text="Branch", font=('Roboto','13','bold'))
canvas2.create_text(300, 230, text="Passout Year", font=('Roboto','13','bold'))


e_srno = ttk.Entry(tab2, width=20, font=('Roboto','13','bold'))
e_srno.place(x=435,y=20)

e_rollno = ttk.Entry(tab2, width=20, font=('Roboto','13','bold'))
e_rollno.place(x=435,y=70)

e_name = ttk.Entry(tab2, width=20, font=('Roboto','13','bold'))
e_name.place(x=435,y=120)

e_branchh = ttk.Combobox(tab2, width=18, state="readonly", font=('Roboto','13','bold'))
e_branchh['values'] = ('Information Technology', 'Computer Engineering', 'Electronics Engineering', 'Electronics and Telecommunication Engineering', 'Biomedical Engineering', 'Management Studies')
e_branchh.place(x=435,y=170)

e_pass = ttk.Combobox(tab2, width=18, state="readonly", font=('Roboto','13','bold'))
e_pass['values'] = (
       '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
       '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024')
e_pass.place(x=435,y=220)

post = Button(tab2, text="  Post  ", bg="blue", fg="white", font="Verdana 12 bold",command=adddb)
post.place(x=200,y=270)
delp = Button(tab2, text="  Delete  ", bg="blue", fg="white", font="Verdana 12 bold",command=delp)
delp.place(x=290,y=270)
importbtn=Button(tab2,text="Import from CSV", bg="blue", fg="white", font="Verdana 12 bold",command=importcsv)
importbtn.place(x=400,y=270)
savedb=Button(tab2,text="  Save Data  ", bg="blue", fg="white", font="Verdana 12 bold",command=savedb)
savedb.place(x=580,y=270)


def showdb():
  try:
    connect4=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor4=connect4.cursor()
    cursor4.execute("SELECT * FROM passout")
    global tree5
    tree5=ttk.Treeview(tab2)

    tree5['show'] = 'headings'
    tree5["columns"]=("SrNo","RollNo","Name","Branch","PassoutYear")
    tree5.column("SrNo", width=80, minwidth=80)
    tree5.column("RollNo",width=150,minwidth=150)
    tree5.column("Name",width=170,minwidth=170)
    tree5.column("Branch",width=250,minwidth=250)
    tree5.column("PassoutYear", width=200, minwidth=200)

    #assign headings
    tree5.heading("SrNo", text="SrNo")
    tree5.heading("RollNo",text="RollNo")
    tree5.heading("Name",text="Name")
    tree5.heading("Branch",text="Branch")
    tree5.heading("PassoutYear", text="PassoutYear")

    i=0
    for ro in cursor4:
        tree5.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4]))
        i=i+1
    tree5.place(x=40,y=320)


  except Exception as e:
    MessageBox.showerror("Backend Error", e)
showdb()


#tab 3
canvas3 = Canvas(tab3, width=600,height=690)
canvas3.pack(fill="both", expand=True)
# Display image
canvas3.create_image(0, 0, image=bg,anchor="nw")
hour_string = StringVar()
min_string = StringVar()

def eventpost():
    get_ename = e_ename.get()
    get_description=e_description.get()
    get_date = e_date.get()
    get_min= min_sb.get()
    get_hr =sec_hour.get()
    get_ampm =e_ampm.get()
    get_time=get_hr+":"+get_min+" "+get_ampm
    get_venue = e_venue.get()

    if get_ename == "" or get_description == "" or get_date == "" or get_time == "" or get_venue == "" :
        MessageBox.showerror("Insert Status", "All fields are required")
    else:
        try:
            connect4 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor4 = connect4.cursor()
            cursor4.execute("Insert into events values(NULL,'" + get_ename + "','" + get_description + "','" + get_date + "','" + get_time + "','" + get_venue + "')")
            cursor4.execute("commit")
            e_eid.delete(0,'end')
            e_ename.delete(0, 'end')
            e_description.delete(0, 'end')
            e_venue.delete(0, 'end')
            MessageBox.showinfo("Post Status", "Job Posted")
            connect4.close()
            showevent()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

canvas3.create_text(300, 30, text="SrNo", font=('Roboto','13','bold'))
canvas3.create_text(300, 80, text="Event Name", font=('Roboto','13','bold'))
canvas3.create_text(300, 130, text="Description", font=('Roboto','13','bold'))
canvas3.create_text(300, 180, text="Date", font=('Roboto','13','bold'))
canvas3.create_text(300, 230, text="Time", font=('Roboto','13','bold'))
canvas3.create_text(300, 280, text="Venue", font=('Roboto','13','bold'))

e_eid = ttk.Entry(tab3,width=20, font=('Roboto','13','bold'))
e_eid.place(x=435,y=30)

e_ename = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_ename.place(x=435,y=80)

e_description = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_description.place(x=435,y=130)

e_date = DateEntry(tab3,selectmode="day", date_pattern='dd-MM-yyyy')
e_date.place(x=435,y=180)

sec_hour = Spinbox(tab3,from_=0,to=23,wrap=True,width=5,justify=CENTER,state="readonly")
sec_hour.place(x=435,y=230)

min_sb = Spinbox(tab3,from_=0,to=59,wrap=True,width=5,state="readonly",justify=CENTER)
min_sb.place(x=490,y=230)

my_list=['AM', 'PM']
e_ampm = Spinbox(tab3,values=my_list,width=5,state="readonly",wrap=True)
e_ampm.place(x=540,y=230)

e_venue = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_venue.place(x=435,y=280)

post = Button(tab3, text="  Post  ", bg="blue", fg="white", font="Verdana 12 bold",command=eventpost)
post.place(x=330, y=310)

deleteb = Button(tab3, text="  Delete  ", bg="blue", fg="white", font="Verdana 12 bold",command=lambda:deletevts())
deleteb.place(x=435,y=310)


def deletevts():
    if e_eid.get() == "":
        MessageBox.showerror("Fetch Status", "ID is compulsory for delete")
    else:
        try:
            connect3 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor3 = connect3.cursor()
            cursor3.execute("delete from events where ID='" + e_eid.get() + "'")
            cursor3.execute("commit");

            e_eid.delete(0, 'end')
            e_ename.delete(0, 'end')
            e_date.delete(0, 'end')
            e_venue.delete(0, 'end')
            showevent()
            MessageBox.showinfo("Delete Status", "Deleted Successfully")
            connect3.close()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)


def showevent():
  try:
    connect3=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor3=connect3.cursor()
    cursor3.execute("SELECT * FROM events")

    tree2=ttk.Treeview(tab3)
    tree2['show'] = 'headings'
    tree2["columns"]=("ID","EventName","Description","Date","Time","Venue")
    tree2.column("ID", width=60, minwidth=60)
    tree2.column("EventName",width=200,minwidth=200)
    tree2.column("Description", width=250, minwidth=250)
    tree2.column("Date",width=100,minwidth=100)
    tree2.column("Time",width=80,minwidth=80)
    tree2.column("Venue",width=200,minwidth=200)

    #assign headings
    tree2.heading("ID", text="ID")
    tree2.heading("EventName",text="EventName")
    tree2.heading("Description", text="Description")
    tree2.heading("Date",text="Date")
    tree2.heading("Time",text="Time")
    tree2.heading("Venue",text="Venue")

    i=0
    for ro in cursor3:
        tree2.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5]))
        i=i+1
    tree2.place(x=20,y=355)

  except Exception as e:
    MessageBox.showerror("Backend Error", e)
showevent()

#Tab 4
canvas4 = Canvas(tab4, width=600,height=690)
canvas4.pack(fill="both", expand=True)
# Display image
canvas4.create_image(0, 0, image=bg,anchor="nw")
def jobdel():
    if e_jid.get() == "":
        MessageBox.showerror("Fetch Status", "ID is compulsory for delete")
    else:
        try:
            connect2 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor2 = connect2.cursor()
            cursor2.execute("delete from jobs where ID='" + e_jid.get() + "'")
            cursor2.execute("commit");
            e_eid.delete(0, 'end')
            e_ename.delete(0, 'end')
            e_date.delete(0, 'end')
            e_venue.delete(0, 'end')
            showjobs()
            MessageBox.showinfo("Delete Status", "Deleted Successfully")
            connect2.close()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

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
            cursor4.execute("Insert into jobs values(NULL,'" + get_company + "','" + get_post + "','" + get_minquali + "','" + get_location + "','" + get_applylink + "')")
            cursor4.execute("commit")

            e_company.delete(0, 'end')
            e_post.delete(0, 'end')
            e_location.delete(0, 'end')
            e_minquali.set('')
            e_applylink.delete(0, 'end')
            MessageBox.showinfo("Post Status", "Job Posted")
            connect4.close()
            showjobs()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

canvas4.create_text(300, 30, text="ID", font=('Roboto','13','bold'))
canvas4.create_text(300, 80, text="Company", font=('Roboto','13','bold'))
canvas4.create_text(300, 130, text="Post", font=('Roboto','13','bold'))
canvas4.create_text(300, 180, text="Min Qualification", font=('Roboto','13','bold'))
canvas4.create_text(300, 230, text="Location", font=('Roboto','13','bold'))
canvas4.create_text(300, 280, text="Apply Link", font=('Roboto','13','bold'))

e_jid = ttk.Entry(tab4, width=20, font=('Roboto','13','bold'))
e_jid.place(x=435,y=20)

e_company = ttk.Entry(tab4, width=20, font=('Roboto','13','bold'))
e_company.place(x=435,y=70)

e_post = ttk.Entry(tab4, width=20, font=('Roboto','13','bold'))
e_post.place(x=435,y=120)

e_minquali = ttk.Combobox(tab4, width=18, state="readonly", font=('Roboto','13','bold'))
e_minquali['values'] = (
'BE/BTech(IT/CO)', 'ME/MTech(IT/CO)', 'BE/BTech(EXTC/ETRX)', 'ME/MTech(EXTC/ETRX)', 'BE/BTech(BIOM)', 'ME/MTech(BIOM)')
e_minquali.place(x=435,y=170)

e_location = ttk.Entry(tab4, width=20, font=('Roboto','13','bold'))
e_location.place(x=435,y=220)

e_applylink = ttk.Entry(tab4, width=20, font=('Roboto','13','bold'))
e_applylink.place(x=435,y=270)

post = Button(tab4, text="  Post  ", bg="blue", fg="white", font="Verdana 12 bold",command=jobpost)
post.place(x=330,y=300)

delb= Button(tab4, text="  Delete  ", bg="blue", fg="white", font="Verdana 12 bold",command=jobdel)
delb.place(x=435,y=300)

def showjobs():
  try:
    connect3=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor3=connect3.cursor()
    cursor3.execute("SELECT * FROM jobs")

    tree2=ttk.Treeview(tab4)
    tree2['show'] = 'headings'
    tree2["columns"]=("ID","Company","Post","MinQuali","Location","ApplyLink")
    tree2.column("ID", width=50, minwidth=50)
    tree2.column("Company",width=140,minwidth=140)
    tree2.column("Post",width=150,minwidth=150)
    tree2.column("MinQuali",width=150,minwidth=150)
    tree2.column("Location",width=150,minwidth=150)
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
    tree2.place(x=20,y=350)

  except Exception as e:
    MessageBox.showerror("Backend Error", e)
showjobs()

root.mainloop()