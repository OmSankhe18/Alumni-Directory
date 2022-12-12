import io
import os
from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkinter import ttk

from PIL import ImageTk,Image
from tkcalendar import DateEntry

root = Tk()
pw = ttk.PanedWindow(root, orient=VERTICAL)
pw.pack(fill=BOTH, expand=True)
frame1 = Frame(pw, relief=SUNKEN, bg="#4169E1")
frame2 = Frame(pw, relief=SUNKEN, bg="#fff")
pw.add(frame1, weight=1)
pw.add(frame2, weight=6)
root.geometry("920x690")
root.title("VIT Alumni Directory | Admin Homepage")
root.iconbitmap("al_icon.ico")

def logout():
    root.destroy()
    os.system("admin_login.py")

#Frame1
label = Label(frame1, text="", bg="#4169E1",fg="#fff", font=('Roboto','15','bold'))
label.place(x=10, y=30)

with open('uname_ad.txt', 'r') as f:
    a=f.read()
label.config(text="Welcome "+a)

label2 = Label(frame1, text="Welcome to Alumni Directory Admin Panel", bg="#4169E1",fg="#fff", font=('Roboto','15','bold'))
label2.place(x=290, y=30)

lg = Button(frame1, text="  Logout  ", bg="blue", fg="white", font=('Roboto','15','bold'), command=logout)
lg.place(x=800, y=25)

#Frame2
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Roboto','13','bold') )
tabControl = ttk.Notebook(frame2)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='  Alumni Report  ')
tabControl.add(tab2, text='  Staff Report  ')
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
    items=tree2.get_children()
    search1=q.get().capitalize()
    for i in items:
        if search1 in tree2.item(i)['values'][1]:
            search_var1=tree2.item(i)['values']
            tree2.delete(i)
            tree2.insert("",0,values=search_var1)

canvas1.create_text(300, 24, text="Search Alumni", font=('Roboto','13','bold'))
q=StringVar()
search = ttk.Entry(tab1, font=('Roboto','13'), textvariable=q)
search.place(x=410, y=12)
q.trace("w", filterSearch)

try:
  connect6=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
  cursor6=connect6.cursor()
  cursor6.execute("SELECT * FROM alumni_login")
  
  def alumni_report():
      global tree2
      tree2 = ttk.Treeview(tab1, style = 'style1.Treeview')
      style1 = ttk.Style(tab1)
      style1.configure("style1.Treeview", rowheight=80)  # set row height
      tree2['columns'] = ("RollNo", "Name", "PassoutYear", "MobileNo", "Branch", "Work Company")
      tree2.column("#0", width=150, stretch='NO', minwidth=150)  # set width
      tree2.column("RollNo", width=100, anchor='w', minwidth=100)
      tree2.column("Name", width=100, anchor='w', minwidth=100)
      tree2.column("PassoutYear", width=100, anchor='w', minwidth=100)
      tree2.column("MobileNo", width=100, anchor='w', minwidth=100)
      tree2.column("Branch", width=150, anchor='w', minwidth=150)
      tree2.column("Work Company", width=150, anchor='w', minwidth=150)

      tree2.heading("#0", anchor='w', text='Image')
      tree2.heading("RollNo", anchor='w', text="RollNo")
      tree2.heading("Name", anchor='w', text="Name")
      tree2.heading("PassoutYear", anchor='w', text="PassoutYear")
      tree2.heading("MobileNo", anchor='w', text="MobileNo")
      tree2.heading("Branch", anchor='w', text="Branch")
      tree2.heading("Work Company", anchor='w', text="Work Company")

      count = 0

      tree2.imglist = []
      for record in cursor6:
          dp = Image.open(io.BytesIO(record[2]))
          dp.thumbnail((80, 80))  # resize the image to desired size
          dp = ImageTk.PhotoImage(dp)
          tree2.insert(parent="", index="end", id=count,
                       image=dp, values=(
              record[0], record[1], record[3], record[4], record[5], record[6],))  # use "image" option for the image
          tree2.imglist.append(dp)  # save the image reference
          count += 1

      for record in cursor6:
          # print(record)
          tree2.insert(parent='', index='end', id=count, text='Parent',
                       values=(record[0]))
          count += 1
      tree2.place(x=40, y=50)

except Exception as e:
    MessageBox.showerror("Backend Error", e)

alumni_report()

al_count = len(tree2.get_children())
al_count_lbl=Label(tab1, text="", font=('Roboto','13','bold'),bg="white")
al_count_lbl.place(x=50,y=520)
al_count_lbl.config(text="Total Alumni Registered: "+str(al_count))

#Tab2
canvas2 = Canvas(tab2, width=600,height=690)
canvas2.pack(fill="both", expand=True)
# Display image
canvas2.create_image(0, 0, image=bg,anchor="nw")

try:
  connect7=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
  cursor7=connect7.cursor()
  cursor7.execute("SELECT * FROM staff_login")
  tree3 = ttk.Treeview(tab2)
  def staff_report():
    tree3['show'] = 'headings'
    tree3["columns"]=("Username","Name","Branch","MobileNo")
    tree3.column("Username",width=160,minwidth=160)
    tree3.column("Name",width=230,minwidth=230)
    tree3.column("Branch",width=250,minwidth=250)
    tree3.column("MobileNo",width=170,minwidth=170)

    #assign headings
    tree3.heading("Username",text="Username")
    tree3.heading("Name",text="Name")
    tree3.heading("Branch",text="Branch")
    tree3.heading("MobileNo",text="MobileNo")

    i=0
    for ro in cursor7:
        tree3.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3]))
        i=i+1

    tree3.place(x=50,y=30)

except Exception as e:
    MessageBox.showerror("Backend Error", e)
staff_report()

st_count = len(tree3.get_children())
st_count_lbl=Label(tab2, text="", font=('Roboto','13','bold'),bg="white")
st_count_lbl.place(x=55,y=520)
st_count_lbl.config(text="Total Staff Registered: "+str(st_count))

#Tab3
canvas3 = Canvas(tab3, width=600,height=690)
canvas3.pack(fill="both", expand=True)
# Display image
canvas3.create_image(0, 0, image=bg,anchor="nw")
def addevent():
    get_id=e_id.get()
    get_eventname = e_eventname.get()
    get_description = e_description.get()
    get_date = e_date.get_date().strftime("%d/%m/%Y")
    get_hr = e_hr.get()
    get_min = e_min.get()
    get_ampm = e_ampm.get()
    get_venue = e_venue.get()
    get_time=get_hr+":"+get_min+" "+get_ampm

    if get_id=="" or get_eventname == "" or get_description == "" or get_date == "" or get_hr == "" or get_min == "" or get_ampm == ""or get_venue == "":
        MessageBox.showerror("Event Status", "All fields are required")
    else:
        try:
            connect1 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor1 = connect1.cursor()
            cursor1.execute("Insert into events values('" + get_id + "','" + get_eventname + "','" + get_description + "','" + get_date + "','" + get_time + "','" + get_venue + "')")
            cursor1.execute("commit")
            e_id.delete(0,'end')
            e_eventname.delete(0, 'end')
            e_description.delete(0, 'end')
            e_venue.delete(0, 'end')
            e_date.delete(0, 'end')
            MessageBox.showinfo("Post Status", "Event Posted")
            connect1.close()
            showevents()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

def deleteevent():
    if e_id.get() == "":
        MessageBox.showerror("Fetch Status", "ID is compulsory for delete")
    else:
        try:
            connect3 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor3 = connect3.cursor()
            cursor3.execute("delete from events where ID='" + e_id.get() + "'")
            cursor3.execute("commit");

            e_id.delete(0, 'end')
            e_eventname.delete(0, 'end')
            e_description.delete(0, 'end')
            e_venue.delete(0, 'end')
            e_date.delete(0, 'end')
            showevents()
            MessageBox.showinfo("Delete Status", "Deleted Successfully")
            connect3.close()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

def getevent():
   e_eventname.delete(0, 'end')
   e_description.delete(0, 'end')
   e_venue.delete(0, 'end')
   if e_id.get() == "":
       MessageBox.showerror("Fetch Status", "ID is compulsory for fetch")
   else:
       try:
           connect4 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
           cursor4 = connect4.cursor()
           cursor4.execute("Select * from events where ID='" + e_id.get() + "'")
           rows = cursor4.fetchall()
           e_date.delete(0, 'end')
           for row in rows:
                e_eventname.insert(0, row[1])
                e_description.insert(0, row[2])
                e_date.insert(0, row[3])
                e_venue.insert(0, row[5])
           connect4.close()
       except Exception as e:
            MessageBox.showerror("Backend Error", e)

def updateevent():
    update_id = e_id.get()
    update_eventname = e_eventname.get()
    update_description=e_description.get()
    update_date=e_date.get_date().strftime("%d/%m/%Y")
    update_hr=e_hr.get()
    update_min = e_min.get()
    update_ampm = e_ampm.get()
    update_venue=e_venue.get()
    update_time = update_hr + ":" + update_min + " " + update_ampm

    if (update_id == "" or update_eventname == "" or update_description == "" or update_date=="" or update_hr=="" or update_min=="" or update_ampm=="" or update_venue==""):
        MessageBox.showerror("Update Status", "All fields are required")
    else:
        connect5 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
        cursor5 = connect5.cursor()
        cursor5.execute("update events set EventName='" + update_eventname + "',Description='" + update_description + "',Date='" + update_date + "',Time='" + update_time + "',Venue='" + update_venue + "' where ID='" + update_id + "'")
        cursor5.execute("commit");

        e_id.delete(0, 'end')
        e_eventname.delete(0, 'end')
        e_description.delete(0, 'end')
        e_venue.delete(0, 'end')
        e_date.delete(0, 'end')
        MessageBox.showinfo("Update Status", "Updated Successfully")
        showevents()
        connect5.close()

canvas3.create_text(300, 30, text="ID", font=('Roboto','13','bold'))
canvas3.create_text(300, 80, text="Event Name", font=('Roboto','13','bold'))
canvas3.create_text(300, 130, text="Description", font=('Roboto','13','bold'))
canvas3.create_text(300, 180, text="Date", font=('Roboto','13','bold'))
canvas3.create_text(300, 230, text="Time", font=('Roboto','13','bold'))
canvas3.create_text(300, 280, text="Venue", font=('Roboto','13','bold'))

e_id = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_id.place(x=435,y=20)

e_eventname = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_eventname.place(x=435,y=70)

e_description = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_description.place(x=435,y=120)

e_date = DateEntry(tab3,selectmode="day", date_pattern='dd-MM-yyyy')
e_date.place(x=435,y=170)

e_hr = Spinbox(tab3, from_= 0, to = 23,width=5,state="readonly",wrap=True)
e_hr.place(x=435,y=220)

e_min = Spinbox(tab3, from_= 0, to = 59,width=5,state="readonly",wrap=True)
e_min.place(x=485,y=220)

my_list=['AM', 'PM']
e_ampm = Spinbox(tab3,values=my_list,width=5,state="readonly",wrap=True)
e_ampm.place(x=530,y=220)

e_venue = ttk.Entry(tab3, width=20, font=('Roboto','13','bold'))
e_venue.place(x=435,y=270)

post = Button(tab3, text="  Post  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=addevent)
post.place(x=250,y=310)
delete = Button(tab3, text="  Delete  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=deleteevent)
delete.place(x= 350,y=310)
update = Button(tab3, text="  Update  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=updateevent)
update.place(x=460,y=310)
get = Button(tab3, text="  Get  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=getevent)
get.place(x=580,y=310)
def showevents():
  try:
    connect2=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor2=connect2.cursor()
    cursor2.execute("SELECT * FROM events")

    tree1=ttk.Treeview(tab3)
    tree1['show'] = 'headings'
    tree1["columns"]=("ID","EventName","Description","Date","Time","Venue")
    tree1.column("ID",width=50,minwidth=50)
    tree1.column("EventName",width=150,minwidth=150)
    tree1.column("Description",width=250,minwidth=250)
    tree1.column("Date",width=100,minwidth=100)
    tree1.column("Time",width=80,minwidth=80)
    tree1.column("Venue",width=200,minwidth=200)

    #assign headings
    tree1.heading("ID",text="ID")
    tree1.heading("EventName",text="EventName")
    tree1.heading("Description",text="Description")
    tree1.heading("Date",text="Date")
    tree1.heading("Time",text="Time")
    tree1.heading("Venue", text="Venue")
    i=0
    for ro in cursor2:
        tree1.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5]))
        i=i+1
    tree1.place(x=50,y=350)

  except Exception as e:
    MessageBox.showerror("Backend Error", e)
showevents()

#Tab4
canvas4 = Canvas(tab4, width=600,height=690)
canvas4.pack(fill="both", expand=True)
# Display image
canvas4.create_image(0, 0, image=bg,anchor="nw")
def showjobs():
  try:
    connect8=mysql.connect(host="localhost",user="root",password="",database="vit_alumni_directory")
    cursor8=connect8.cursor()
    cursor8.execute("SELECT * FROM jobs")

    tree4=ttk.Treeview(tab4)
    tree4['show'] = 'headings'
    tree4["columns"]=("ID","Company","Post","MinQuali","Location","ApplyLink")
    tree4.column("ID", width=50, minwidth=50)
    tree4.column("Company",width=130,minwidth=130)
    tree4.column("Post",width=150,minwidth=150)
    tree4.column("MinQuali",width=150,minwidth=150)
    tree4.column("Location",width=150,minwidth=150)
    tree4.column("ApplyLink",width=250,minwidth=250)

    #assign headings
    tree4.heading("ID", text="ID")
    tree4.heading("Company",text="Company")
    tree4.heading("Post",text="Post")
    tree4.heading("MinQuali",text="MinQuali")
    tree4.heading("Location",text="Location")
    tree4.heading("ApplyLink",text="ApplyLink")

    i=0
    for ro in cursor8:
        tree4.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5]))
        i=i+1
    tree4.place(x=20,y=350)

  except Exception as e:
    MessageBox.showerror("Backend Error", e)
showjobs()

def getjob():
   e_company.delete(0, 'end')
   e_post.delete(0, 'end')
   e_minquali.set('')
   e_location.delete(0, 'end')
   e_applylink.delete(0,'end')
   if e_jobid.get() == "":
       MessageBox.showerror("Fetch Status", "ID is compulsory for fetch")
   else:
       try:
           connect9 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
           cursor9 = connect9.cursor()
           cursor9.execute("Select * from jobs where ID='" + e_jobid.get() + "'")
           rows = cursor9.fetchall()
           for row in rows:
                e_company.insert(0, row[1])
                e_post.insert(0, row[2])
                e_minquali.set(row[3])
                e_location.insert(0, row[4])
                e_applylink.insert(0, row[5])
           connect9.close()
       except Exception as e:
            MessageBox.showerror("Backend Error", e)

def deletejob():
    if e_jobid.get() == "":
        MessageBox.showerror("Fetch Status", "ID is compulsory for delete")
    else:
        try:
            connect10 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor10 = connect10.cursor()
            cursor10.execute("delete from jobs where ID='" + e_jobid.get() + "'")
            cursor10.execute("commit");
            e_jobid.delete(0, 'end')
            e_company.delete(0, 'end')
            e_post.delete(0, 'end')
            e_minquali.set('')
            e_location.delete(0, 'end')
            e_applylink.delete(0, 'end')
            showjobs()
            MessageBox.showinfo("Delete Status", "Deleted Successfully")
            connect10.close()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

def updatejob():
    update_jobid = e_jobid.get()
    update_company = e_company.get()
    update_post = e_post.get()
    update_minquali = e_minquali.get()
    update_location = e_location.get()
    update_applylink = e_applylink.get()

    if update_jobid == "" or update_company == "" or update_post == "" or update_minquali=="" or update_location=="" or update_applylink=="":
        MessageBox.showerror("Update Status", "All fields are required")
    else:
        connect11 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
        cursor11 = connect11.cursor()
        cursor11.execute("update jobs set Company='" + update_company + "',Post='" + update_post + "',MinQuali='" + update_minquali + "',Location='" + update_location + "',ApplyLink='" + update_applylink + "' where ID='" + update_jobid + "'")
        cursor11.execute("commit");

        e_company.delete(0, 'end')
        e_post.delete(0, 'end')
        e_minquali.set('')
        e_location.delete(0, 'end')
        e_applylink.delete(0, 'end')
        MessageBox.showinfo("Update Status", "Updated Successfully")
        showjobs()
        connect11.close();

def addjob():
    get_company = e_company.get()
    get_post = e_post.get()
    get_minquali = e_minquali.get()
    get_location = e_location.get()
    get_applylink = e_applylink.get()

    if get_company == "" or get_post == "" or get_minquali == "" or get_location == "" or get_applylink == "":
        MessageBox.showerror("Job Status", "All fields are required")
    else:
        try:
            connect1 = mysql.connect(host="localhost", user="root", password="", database="vit_alumni_directory")
            cursor1 = connect1.cursor()
            cursor1.execute("Insert into jobs values(NULL,'" + get_company + "','" + get_post + "','" + get_minquali + "','" + get_location + "','" + get_applylink + "')")
            cursor1.execute("commit")
            e_jobid.delete(0,'end')
            e_company.delete(0, 'end')
            e_post.delete(0, 'end')
            e_minquali.delete(0, 'end')
            e_location.delete(0, 'end')
            e_applylink.delete(0, 'end')
            MessageBox.showinfo("Job Status", "Job Posted")
            connect1.close()
            showjobs()
        except Exception as e:
            MessageBox.showerror("Backend Error", e)

canvas4.create_text(300, 30, text="ID", font=('Roboto','13','bold'))
canvas4.create_text(300, 80, text="Company", font=('Roboto','13','bold'))
canvas4.create_text(300, 130, text="Post", font=('Roboto','13','bold'))
canvas4.create_text(300, 180, text="Min Qualification", font=('Roboto','13','bold'))
canvas4.create_text(300, 230, text="Location", font=('Roboto','13','bold'))
canvas4.create_text(300, 280, text="Apply Link", font=('Roboto','13','bold'))

e_jobid = ttk.Entry(tab4, width=20, font=('Roboto','13','bold'))
e_jobid.place(x=435,y=20)

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

postb = Button(tab4, text="  Post  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=addjob)
postb.place(x=250,y=310)
deleteb = Button(tab4, text="  Delete  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=deletejob)
deleteb.place(x= 350,y=310)
updateb = Button(tab4, text="  Update  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=updatejob)
updateb.place(x=460,y=310)
getb = Button(tab4, text="  Get  ", bg="blue", fg="white", font=('Roboto','13','bold'),command=getjob)
getb.place(x=580,y=310)


root.mainloop()