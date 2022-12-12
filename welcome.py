from tkinter import *
import os

def staff():
    root.destroy()
    os.system('staff_login.py')

def alumni():
    root.destroy()
    os.system('alumni_login.py')

def admin():
    root.destroy()
    os.system('admin_login.py')

root = Tk()
root.geometry("600x500")
root.title("VIT Alumni Directory")
root.configure(bg='#ADD8E6')
root.iconbitmap("al_icon.ico")
bg = PhotoImage(file="backg.png")

canvas1 = Canvas(root, width=600,height=690)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg,anchor="nw")

canvas1.create_text(300, 40, text="Welcome to Alumni Directory", font=('Roboto','20','bold'))

f=PhotoImage(file="VIT2.png")
img=canvas1.create_image(200,200,image=f,anchor='sw')

canvas1.create_text(300, 230, text="Once a VITian, Always a VITian", font=('Roboto','15','bold'))

canvas1.create_text(300, 310, text="Select Your Role", font=('Roboto','15','bold'))

staff=Button(root,text="  Staff   ",bg="blue",fg="white", font=('Roboto','14','bold'),command=staff)
staff.place(x=150,y=350)

alumni=Button(root,text="  Alumni  ",bg="blue",fg="white", font=('Roboto','14','bold'),command=alumni)
alumni.place(x=240,y=350)

admin=Button(root,text="  Admin   ",bg="blue",fg="white", font=('Roboto','14','bold'),command=admin)
admin.place(x=350,y=350)

root.mainloop()