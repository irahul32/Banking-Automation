#!/usr/bin/env python
# coding: utf-8

# In[34]:


from tkinter import *
import time
from datetime import datetime
from PIL import Image,ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox,filedialog
import sqlite3
import gmail
import re
import random
from tkinter.ttk import Treeview,Style,Scrollbar
import shutil,os

#database connection
try:
    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_uid text unique,acn_name text,acn_pass text,acn_mob text,acn_email text,acn_gender text,acn_type text,acn_bal float,acn_opendate text)")
    curobj.execute("create table txn_history(acn_no integer,txn_amt float,txn_type float,txn_date text,updated_bal float)")

# Uncomment these code and run once to set the autoincrement sequence and then comment out these lines again
    #curobj.execute("""INSERT INTO acn (acn_no, acn_uid, acn_name, acn_pass, acn_mob, acn_email, acn_gender, acn_type, acn_bal, acn_opendate)
    #VALUES (200193010001, 'rk', 'rahul', '1234', '1234', 'efg', 'male', 'saving', 1200, '3-7-2024')""")
    #curobj.execute("delete from acn")
    conobj.commit()
    conobj.close()
    print("table created")
    
except:
    print("something went wrong,table might already exists!")

win=Tk()
win.title("Net Banking")
win.state('zoomed')
win.configure(bg='#7E2553')
win.resizable(width=False,height=False)

#Name & logo of the bank
title=Label(win,text="Civitas Bank",font=('arial',40,'bold','underline'),bg="#7E2553",fg='white')
title.pack()

logoimg=Image.open('images/logo.jpeg')
logoimg=logoimg.resize((50,54))
logoimgtk=ImageTk.PhotoImage(logoimg,master=win)

lbl_logoimg=Label(win,image=logoimgtk,bg="#7E2553")
lbl_logoimg.place(relx=0.36,rely=0.01)

lbl_date=Label(win,text=f"{datetime.now().date()}",bg='#7E2553',font=('arial',20,'bold'),fg='white')
lbl_date.place(relx=.90,rely=.07)

#main screen
def main_screen():
    frm=Frame(win)
    frm.place(relx=0,rely=0.13,relwidth=1,relheight=0.87)
    #background image
    bg=Image.open('images/bg.jpeg')
    bg=bg.resize((1600,800))
    bgtk=ImageTk.PhotoImage(bg,master=frm)
    lbl_bg=Label(frm,image=bgtk)
    lbl_bg.image = bgtk
    lbl_bg.place(relx=0,rely=0,relwidth=1,relheight=1)
    
    def forgotpass():
        frm.destroy()
        forgotpass_screen()
        
    def newuser():
        frm.destroy()
        newuser_screen()
    
    def welcome():
        global guname,gname,gacn
        guname=e_uid.get()
        pwd=e_pass.get()
        if len(guname)==0 or len(pwd)==0:
            messagebox.showwarning("Empty feilds","Empty fields are not not allowed!")
            return
        else:
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_name,acn_no from acn where acn_uid=? and acn_pass=?",(guname,pwd))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Error","Invalid Username/password")
                return
            else:
                gname=tup[0]
                gacn=tup[1]
                frm.destroy()
                welcome_screen()
        
    def clear():
        e_uid.delete(0,'end')
        e_pass.delete(0,'end')
        e_uid.focus()
    
    ifrm=Frame(frm,highlightbackground='black', highlightthickness=2)
    ifrm.configure(bg='white')
    ifrm.place(relx=.3,rely=.07,relwidth=.5,relheight=.55)
    
    lbl_uid=Label(ifrm,text="Username",font=('arial',20,'bold'),bg='white',fg='#1D2B53')
    lbl_uid.place(relx=0.1,rely=0.1)
    
    e_uid=Entry(ifrm,font=('arial',20,'bold'),bd=5)
    e_uid.place(relx=0.33,rely=0.1)
    e_uid.focus()
    
    lbl_pass=Label(ifrm,text="Password",font=('arial',20,'bold'),bg='white',fg='#1D2B53')
    lbl_pass.place(relx=0.1,rely=0.28)
    
    e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=0.33,rely=0.28)
    
    btn_login=Button(ifrm,text="Login",command=welcome,font=('arial',18,'bold'),bd=5,fg='dark blue')
    btn_login.place(relx=0.37,rely=0.43)
    
    btn_clr=Button(ifrm,text="Clear",font=('arial',18,'bold'),command=clear,bd=5,fg='dark blue')
    btn_clr.place(relx=0.57,rely=0.43)
    
    btn_fp=Button(ifrm,text="Forgot password",command=forgotpass,width=18,font=('arial',18,'bold'),bd=5,fg='dark blue')
    btn_fp.place(relx=0.34,rely=0.63)
    
    btn_open=Button(ifrm,text="Open new account",command=newuser,width=18,font=('arial',18,'bold'),bd=5,fg='dark blue')
    btn_open.place(relx=0.34,rely=0.83)

#Forgot password screen
def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg='#EEF7FF')
    frm.place(relx=0,rely=0.13,relwidth=1,relheight=1)
    lbl_frmtitle=Label(frm,text="Forgot Password Screen",bg='#EEF7FF',font=('arial',25,'bold'),fg='#fd5c63')
    lbl_frmtitle.pack()
    
    def back():
        frm.destroy()
        main_screen()
   
    def forgotpass():
        uid=e_uid.get()
        mob=e_mob.get()
        email=e_email.get()
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from acn where acn_uid=? and acn_mob=? and acn_email=?",(uid,mob,email))
        tup=curobj.fetchone()
        conobj.close()
        
        if tup==None:
            messagebox.showerror("Password","Details not found!")
            return
        else:
            otp=random.randint(1000,9999)
            con=gmail.GMail("rahul8022raj@gmail.com","shrf ubdp vtfn tvtp")
            msg=gmail.Message(to=email,subject="Password Recovery",text=f"Your One Time Password(OTP) is: {otp}\nDo not share this OTP with anyone.")
            con.send(msg)
            messagebox.showinfo("Password","OTP sent,check your mail")
            
            lbl_otp=Label(frm,text="OTP",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
            lbl_otp.place(relx=0.3,rely=0.5)
        
            e_otp=Entry(frm,font=('arial',20,'bold'),bd=5)
            e_otp.place(relx=0.3,rely=0.55)
            e_otp.focus()
        
        def resetpass_db():
            verify_otp=int(e_otp.get())
            if verify_otp==otp:
                frm.destroy()
                frm2=Frame(win)
                frm2.configure(bg='#EEF7FF')
                frm2.place(relx=0,rely=0.13,relwidth=1,relheight=1)
                lbl_frmtitle=Label(frm2,text="Reset Your Password",bg='#EEF7FF',font=('arial',25,'bold'),fg='#fd5c63')
                lbl_frmtitle.pack()

                lbl_pass=Label(frm2,text="Password",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
                lbl_pass.place(relx=0.2,rely=0.13)

                e_pass=Entry(frm2,font=('arial',20,'bold'),bd=5,show='*')
                e_pass.place(relx=0.37,rely=0.13)

                lbl_repass=Label(frm2,text="Confirm Password",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
                lbl_repass.place(relx=0.2,rely=0.23)

                e_repass=Entry(frm2,font=('arial',20,'bold'),bd=5,show='*')
                e_repass.place(relx=0.37,rely=0.23)

                def reset_db():
                    pwd=e_pass.get()
                    re_pwd=e_repass.get()
                    if pwd==re_pwd:
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        curobj.execute("update acn set acn_pass=? where acn_uid=?",(pwd,uid))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("Password","Password changed successfully")
                        forgotpass_screen()
                    else:
                        messagebox.showwarning("Password","Please enter same password!")
                        return
                
                btn_reset=Button(frm2,text="Reset",command=reset_db,font=('arial',20,'bold'),bd=5,fg='dark blue')
                btn_reset.place(relx=0.4,rely=0.3)
                
                def cancel():
                    forgotpass_screen()

                btn_cancel=Button(frm2,text="Cancel",command=cancel,font=('arial',20,'bold'),bd=5,fg='dark blue')
                btn_cancel.place(relx=0.49,rely=0.3)
            
            else:
                messagebox.showerror("Password","OTP doesn't match!")
                return
        
        btn_verify=Button(frm,text="Verify",command=resetpass_db,font=('arial',20,'bold'),bd=5,fg='dark blue')
        btn_verify.place(relx=0.43,rely=0.62)
        
    def clear():
        e_uid.delete(0,'end')
        e_mob.delete(0,'end')
        e_email.delete(0,'end')
        e_uid.focus()
        
    btn_back=Button(frm,text='back',font=('arial',20,'bold'),command=back)
    btn_back.place(relx=0,rely=0)
    
    lbl_uid=Label(frm,text="Username",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_uid.place(relx=0.2,rely=0.1)
    
    e_uid=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_uid.place(relx=0.35,rely=0.1)
    e_uid.focus()
    
    lbl_mob=Label(frm,text="Mobile",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_mob.place(relx=0.2,rely=0.2)
    
    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=0.35,rely=0.2)
    
    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_email.place(relx=0.2,rely=0.3)
    
    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=0.35,rely=0.3)
    
    btn_sub=Button(frm,text="Send OTP",command=forgotpass,font=('arial',20,'bold'),bd=5,fg='dark blue')
    btn_sub.place(relx=0.36,rely=0.4)
    
    btn_clear=Button(frm,text="Clear",command=clear,font=('arial',20,'bold'),bd=5,fg='dark blue')
    btn_clear.place(relx=0.49,rely=0.4)

#open new account screen
def newuser_screen():
    frm=Frame(win)
    frm.configure(bg='#EEF7FF')
    frm.place(relx=0,rely=0.13,relwidth=1,relheight=1)
    lbl_frmtitle=Label(frm,text="Open New Account Screen",bg='#EEF7FF',font=('arial',25,'bold'),fg='#fd5c63')
    lbl_frmtitle.pack()
    
    def back():
        frm.destroy()
        main_screen()
        
    def newuser_db():
        uid=e_uid.get()
        name=e_name.get().title()
        pwd=e_pass.get()
        repwd=e_repass.get()
        mob=e_mob.get()
        email=e_email.get()
        gender=cb_gender.get()
        acntype=cb_type.get()
        bal=1000
        opendate=datetime.now().date()
        
        #Data validation
        if uid=="" or name=="" or pwd=="" or repwd=="" or mob=="" or email=="" or gender=="" or acntype=="":
            messagebox.showwarning("Empty Feilds","Empty fields are not allowed !")
            return
        
        match=re.fullmatch("[A-Z][a-z]+[0-9]+",uid)
        if match==None:
            messagebox.showerror("Username","Invalid format of username")
            return
        
        if pwd!=repwd:
            messagebox.showwarning("Password","Please enter same password!")
            return
        
        match=re.fullmatch("[6-9]\d{9}",mob)
        if match==None:
            messagebox.showerror("Mobile","Invalid format of mobile")
            return
        
        match=re.fullmatch("\w+@[a-zA-Z]{2,6}\.[a-zA-Z]{2,3}",email)
        if match==None:
            messagebox.showerror("Email","Invalid format of email")
            return   
        
        try:
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute(""" insert into acn(acn_uid,acn_name,acn_pass,acn_mob,acn_email,acn_gender,acn_type,acn_bal,acn_opendate)
                           values(?,?,?,?,?,?,?,?,?)""",(uid,name,pwd,mob,email,gender,acntype,bal,opendate))
            conobj.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Username","This username already taken!")
            return
        finally:
            conobj.close()
        
        #Account created pop box and account number sent to gmail
        messagebox.showinfo("New User","Congratulation, Account created successfully!")
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        conobj.close()
        
        #sending gmail
        con=gmail.GMail("rahul8022raj@gmail.com","shrf ubdp vtfn tvtp")
        msg=gmail.Message(to=email,subject="Welcome message",text=f"Thank you for opening your account in CIVITAS Bank!\nYour account number is : {tup[0]}\nDon't share your account number with anyone!")
        con.send(msg)
        print("done")
        
        e_name.delete(0,'end')
        e_uid.delete(0,'end')
        e_pass.delete(0,'end')
        e_repass.delete(0,'end')
        e_mob.delete(0,'end')
        e_email.delete(0,'end')
        cb_gender.delete(0,'end')
        cb_type.delete(0,'end')
        e_name.focus()
    
    def clear():
        e_name.delete(0,'end')
        e_uid.delete(0,'end')
        e_pass.delete(0,'end')
        e_repass.delete(0,'end')
        e_mob.delete(0,'end')
        e_email.delete(0,'end')
        cb_gender.delete(0,'end')
        cb_type.delete(0,'end')
        e_name.focus()
    
    btn_back=Button(frm,text='back',font=('arial',20,'bold'),command=back)
    btn_back.place(relx=0,rely=0)
    
    lbl_name=Label(frm,text="Name",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_name.place(relx=0.2,rely=0.08)
    
    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=0.37,rely=0.08)
    e_name.focus()
    
    lbl_uid=Label(frm,text="Username",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_uid.place(relx=0.2,rely=0.16)
    
    e_uid=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_uid.place(relx=0.37,rely=0.16)
    
    lbl_msg=Label(frm,text="(Username must contain atleast 1 capital letter & number)",font=('arial',10,'bold'),bg='#EEF7FF',fg='red')
    lbl_msg.place(relx=0.369,rely=0.2)
    
    lbl_pass=Label(frm,text="Password",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_pass.place(relx=0.2,rely=0.24)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=0.37,rely=0.24)
    
    lbl_repass=Label(frm,text="Re-type Password",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_repass.place(relx=0.2,rely=0.32)
    
    e_repass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_repass.place(relx=0.37,rely=0.32)
    
    lbl_mob=Label(frm,text="Mobile",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_mob.place(relx=0.2,rely=0.4)
    
    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=0.37,rely=0.4)
    
    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_email.place(relx=0.2,rely=0.48)
    
    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=0.37,rely=0.48)
    
    lbl_gender=Label(frm,text="Gender",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_gender.place(relx=0.2,rely=0.56)
    
    cb_gender=Combobox(frm,values=['----select----','Male','Female','Others'],font=('arial',20,'bold'))
    cb_gender.place(relx=0.37,rely=0.56) 
    
    lbl_type=Label(frm,text="Account type",font=('arial',20,'bold'),bg='#EEF7FF',fg='#240750')
    lbl_type.place(relx=0.2,rely=0.64)
    
    cb_type=Combobox(frm,values=['----select----','Saving','Current'],font=('arial',20,'bold'))
    cb_type.place(relx=0.37,rely=0.64)
    
    btn_sub=Button(frm,text="Submit",command=newuser_db,font=('arial',20,'bold'),bd=5,fg='dark blue')
    btn_sub.place(relx=0.4,rely=0.75)
    
    btn_clear=Button(frm,text="Clear",command=clear,font=('arial',20,'bold'),bd=5,fg='dark blue')
    btn_clear.place(relx=0.51,rely=0.75)

#login Screen
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='#EEF7FF')
    frm.place(relx=0,rely=0.13,relwidth=1,relheight=1)
    
    def logout():
        #global lbl_welcome
        lbl_welcome.destroy()
        #frm.destroy()
        main_screen()
        
    def details():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.5)
        lbl_frmtitle.configure(text="This is Check Details Screen")
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from acn where acn_uid=?",(guname,))
        tup=curobj.fetchone()
        conobj.close()
        
        lbl_acn=Label(ifrm,text=f"Account no. :\t\t{tup[0]}",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_acn.place(relx=0.2,rely=0.05)
        
        lbl_name=Label(ifrm,text=f"Account Holder's Name :\t{tup[2]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_name.place(relx=0.2,rely=0.15)
        
        lbl_uid=Label(ifrm,text=f"Username :\t\t{tup[1]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_uid.place(relx=0.2,rely=0.25)
        
        lbl_mob=Label(ifrm,text=f"Mobile :\t\t\t{tup[4]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_mob.place(relx=0.2,rely=0.35)
        
        lbl_email=Label(ifrm,text=f"Email :\t\t\t{tup[5]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_email.place(relx=0.2,rely=0.45)
        
        lbl_type=Label(ifrm,text=f"Available type :\t\t{tup[7]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_type.place(relx=0.2,rely=0.55)
        
        lbl_bal=Label(ifrm,text=f"Available balance :\t{tup[8]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_bal.place(relx=0.2,rely=0.65)
        
        lbl_opendate=Label(ifrm,text=f"Account Opendate :\t{tup[9]} ",font=('arial',15,'bold'),bg='white',fg='#240750')
        lbl_opendate.place(relx=0.2,rely=0.75)
        
    def update():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.5)
        lbl_frmtitle.configure(text="This is Update Profile Screen")
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_pass,acn_email,acn_mob from acn where acn_uid=?",(guname,))
        tup=curobj.fetchone()
        conobj.close()
        
        lbl_name=Label(ifrm,text="Name",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_name.place(relx=0.1,rely=0.15)
        
        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=0.09,rely=0.25)
        e_name.insert(0,tup[0])
        
        lbl_pass=Label(ifrm,text="Password",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_pass.place(relx=0.1,rely=0.45)
        
        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pass.place(relx=0.09,rely=0.55)
        e_pass.insert(0,tup[1])
        
        lbl_email=Label(ifrm,text="Email",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_email.place(relx=0.52,rely=0.15)
        
        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=0.51,rely=0.25)
        e_email.insert(0,tup[2])
        
        lbl_mob=Label(ifrm,text="Mobile",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_mob.place(relx=0.52,rely=0.45)
        
        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=0.51,rely=0.55)
        e_mob.insert(0,tup[3])
        
        def update_db():
            name=e_name.get().title()
            pwd=e_pass.get()
            mob=e_mob.get()
            email=e_email.get()
            
            #check validation on mob and email
            match=re.fullmatch("[6-9]\d{9}",mob)
            if match==None:
                messagebox.showerror("Mobile","Invalid format of mobile")
                return
        
            match=re.fullmatch("\w+@[a-zA-Z]{2,6}\.[a-zA-Z]{2,3}",email)
            if match==None:
                messagebox.showerror("Email","Invalid format of email")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_pass=?,acn_mob=?,acn_email=? where acn_uid=?",(name,pwd,mob,email,guname))
            conobj.commit()
            conobj.close()
            
            messagebox.showinfo("Update","Record updated successfully")
            lbl_welcome.destroy()
            welcome_screen()
        
        btn_update=Button(ifrm,text='Update',font=('arial',20,'bold'),command=update_db,bd=5,fg="darkblue")
        btn_update.place(relx=0.75,rely=0.7)
        
    def deposit():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.5)
        lbl_frmtitle.configure(text="This is Deposit Screen")
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_amt.place(relx=0.2,rely=0.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=0.4,rely=0.2)
        e_amt.focus()
        
        def deposit_db():
            amt=float(e_amt.get())
            if amt<0:
                messagebox.showwarning("Amount","Ammount can't be negative")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_bal=acn_bal+? where acn_uid=?",(amt,guname))
            curobj.execute("select acn_bal from acn where acn_uid=?",(guname,))
            tup=curobj.fetchone()
            curobj.execute("insert into txn_history values(?,?,?,?,?)",(gacn,amt,"Credit",time.ctime(),tup[0]))
            conobj.commit()
            conobj.close()
            
            messagebox.showinfo("Deposit",f"Ammount {amt} successfully deposited")
            lbl_welcome.destroy()
            welcome_screen()
        
        btn_deposit=Button(ifrm,text='Deposit',font=('arial',20,'bold'),command=deposit_db,bd=5,fg="darkblue")
        btn_deposit.place(relx=0.64,rely=0.4) 
        
    def withdraw():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.5)
        lbl_frmtitle.configure(text="This is Withdraw Screen")
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_amt.place(relx=0.2,rely=0.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=0.4,rely=0.2)
        e_amt.focus()
        
        def withdraw_db():
            amt=float(e_amt.get())
            if amt<0:
                messagebox.showwarning("Amount","Ammount can't be negative")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_uid=?",(guname,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()
            
            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_uid=?",(amt,guname))
                curobj.execute("insert into txn_history values(?,?,?,?,?)",(gacn,amt,"Debit",time.ctime(),avail_bal-amt))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"Ammount {amt} withdrawn successfully")
                lbl_welcome.destroy()
                welcome_screen()
            else:
                messagebox.showwarning("Withdraw","Insufficient balance!")
            
        
        btn_withdraw=Button(ifrm,text='Withdraw',font=('arial',20,'bold'),command=withdraw_db,bd=5,fg="darkblue")
        btn_withdraw.place(relx=0.6,rely=0.4)
        
    def transfer():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.5)
        lbl_frmtitle.configure(text="This is Transfer Screen")
        
        lbl_to=Label(ifrm,text="To",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_to.place(relx=0.2,rely=0.2)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=0.4,rely=0.2)
        e_to.focus()
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),bg='white',fg='#240750')
        lbl_amt.place(relx=0.2,rely=0.4)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=0.4,rely=0.4)
        
        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_amt.get())
            
            if gacn==to_acn:
                messagebox.showerror("Transfer","Sender & receiver account can't be same")
                return
            
            if amt<0:
                messagebox.showwarning("Amount","Ammount can't be negative")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(to_acn,))
            tup=curobj.fetchone()
            curobj.close()
            if tup==None:
                messagebox.showerror("Transfer","Receiver account number does not exist")
                return
            else:
                to_bal=tup[0]
                curobj=conobj.cursor()
                curobj.execute("select acn_bal from acn where acn_uid=?",(guname,))
                tup=curobj.fetchone()
                avail_bal=tup[0]   
                curobj.close()
                if avail_bal>=amt:
                    curobj=conobj.cursor()
                    curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                    curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,to_acn))
                    curobj.execute("insert into txn_history values(?,?,?,?,?)",(gacn,amt,"Debit",time.ctime(),avail_bal-amt))
                    curobj.execute("insert into txn_history values(?,?,?,?,?)",(to_acn,amt,"Credit",time.ctime(),to_bal+amt))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Transfer",f"Ammount {amt} transferred to account number {to_acn} successfully")
                    lbl_welcome.destroy()
                    welcome_screen()
                else:
                    messagebox.showwarning("Transfer","Insufficient balance!")
            
        
        btn_transfer=Button(ifrm,text='Transfer',font=('arial',20,'bold'),command=transfer_db,bd=5,fg="darkblue")
        btn_transfer.place(relx=0.62,rely=0.6)
        
    def txn():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.5)
        lbl_frmtitle.configure(text="This is Txn History Screen")
        
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,height=250,width=700)
        
        style =Style()
        style.configure("Treeview.Heading", font=('arial', 20, 'bold'), foreground='dark blue')
        
        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(x=690,y=0,height=250)
        tv.configure(yscrollcommand=sb.set)
        
        tv['columns']=('col1','col2','col3','col4')
        tv.column('col1',width=150,anchor='c')
        tv.column('col2',width=100,anchor='c')
        tv.column('col3',width=100,anchor='c')
        tv.column('col4',width=100,anchor='c')
        
        tv.heading('col1',text='Date')
        tv.heading('col2',text='Amount')
        tv.heading('col3',text='Type')
        tv.heading('col4',text='Balance')
        
        tv['show']='headings'
   
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from txn_history where acn_no=?",(gacn,))
        for row in curobj:
            tv.insert(parent='',index=0,values=(row[3],row[1],row[2],row[4]))
        conobj.close()
    
    index=gname.index(" ")
    global lbl_welcome,lbl_frmtitle
    lbl_welcome=Label(win,text=f"Welcome,{gname[:index]}",font=('arial',20,'bold'),bg='#7E2553',fg='white')
    lbl_welcome.place(relx=0,rely=0.08)
    
    lbl_frmtitle=Label(frm,text="This is Login Account Screen",bg='#EEF7FF',font=('arial',25,'bold'),fg='#fd5c63')
    lbl_frmtitle.pack()
    
    btn_logout=Button(frm,text='Logout',font=('arial',20,'bold'),command=logout,bd=5,fg="darkblue")
    btn_logout.place(relx=0.91,rely=0.01)
    
    global lbl_img,img,imgtk
    if os.path.exists(f"images/{str(gacn)[-2:]}.jpeg"):
        img=Image.open(f"images/{str(gacn)[-2:]}.jpeg").resize((200,190))
        imgtk=ImageTk.PhotoImage(img,master=win)
    else:
        img=Image.open("images/default.jpeg").resize((200,190))
        imgtk=ImageTk.PhotoImage(img,master=win)
    
    lbl_img=Label(frm,image=imgtk)
    lbl_img.place(relx=0.01,rely=0.01)
    
    def update_pic():
        img=filedialog.askopenfilename()
        shutil.copy(img,f"images/{str(gacn)[-2:]}.jpeg")
        img=Image.open(f"images/{str(gacn)[-2:]}.jpeg").resize((200,190))
        imgtk=ImageTk.PhotoImage(img,master=win)
        lbl_img.image=imgtk
        lbl_img['image']=imgtk
    
    btn_profpic=Button(frm,text='Update Pic',command=update_pic,font=('arial',15,'bold'),bd=5,bg='white',fg='blue')
    btn_profpic.place(relx=.15,rely=.18)
  
    btn_details=Button(frm,text='Check Details',width=12,font=('arial',20,'bold'),command=details,bg='white',bd=5,fg='blue')
    btn_details.place(relx=0,rely=0.25)
    
    btn_update=Button(frm,text='Update Profile',width=12,font=('arial',20,'bold'),command=update,bg='white',bd=5,fg='blue')
    btn_update.place(relx=0,rely=0.35)
    
    btn_deposit=Button(frm,text='Deposit',width=12,font=('arial',20,'bold'),command=deposit,bg='white',bd=5,fg='blue')
    btn_deposit.place(relx=0,rely=0.45)
    
    btn_withdraw=Button(frm,text='Withdraw',width=12,font=('arial',20,'bold'),command=withdraw,bg='white',bd=5,fg='blue')
    btn_withdraw.place(relx=0,rely=0.55)
    
    btn_transfer=Button(frm,text='Transfer',width=12,font=('arial',20,'bold'),command=transfer,bg='white',bd=5,fg='blue')
    btn_transfer.place(relx=0,rely=0.65)
    
    btn_txn=Button(frm,text='Txn history',width=12,font=('arial',20,'bold'),command=txn,bg='white',bd=5,fg='blue')
    btn_txn.place(relx=0,rely=0.75)
    
main_screen()
win.mainloop()


# In[ ]:




