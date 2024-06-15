import sqlite3
from tkinter import *
from tkinter.ttk import Combobox
from datetime import datetime
import time
from tkinter import messagebox,filedialog
import random
import gmail
from tkinter.ttk import Style,Treeview,Scrollbar
from PIL import Image,ImageTk
import shutil
import os


try:
    con=sqlite3.connect(database="banking.sqlite")
    cur=con.cursor()
    cur.execute("create table accounts(acn integer primary key autoincrement,name text,password text,email text,mob text,bal float,type text,opendate text)")
    cur.execute("create table txn_history(acn int,txn_amt float,txn_type float,txn_date text,update_bal float)")
    con.commit()
    print("tables created")
except:
    print("something went wrong,migh be tables already exist")
con.close()



win=Tk()
win.state("zoomed")
win.resizable(width=False,height=True)
win.configure(bg='powder blue')

lbl_title=Label(win,text="Banking Automation",bg='powder blue',fg='blue',font=('arial',60,'bold','underline'))
lbl_title.pack()

lbl_date=Label(win,text=f"{datetime.now().date()}",bg='powder blue',font=('arial',15,'bold'))
lbl_date.place(relx=.9,rely=.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.85)

    def forgot_pass():
        frm.destroy()
        forgotpass_screen()
        
    def open_account():
        frm.destroy()
        openaccount_screen()
    
    def login_account():
        global name,acn
        acn=entry_acn.get()
        pwd=entry_pass.get()
        if(acn=="" or pwd==""):
            messagebox.showerror("Login","ACN/PASS can't be empty")
            return
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select name from accounts where acn=? and password=?",(acn,pwd))
        row=cur.fetchone()
        con.close()
        if(row==None):
            messagebox.showerror("Login","Invalid ACN/PASS")
        else:
            name=row[0]
            frm.destroy()
            loginaccount_screen()
    def reset():
        entry_acn.delete(0,"end")
        entry_pass.delete(0,"end")
        entry_acn.focus()
        
    lbl_acn=Label(frm,text="ACN",bg='pink',font=('arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.1)
    
    entry_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_acn.place(relx=.4,rely=.1)
    entry_acn.focus()
    
    lbl_pass=Label(frm,text="PASS",bg='pink',font=('arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.2)
    
    entry_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    entry_pass.place(relx=.4,rely=.2)
    
    btn_login=Button(frm,command=login_account,text="login",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_login.place(relx=.43,rely=.3)
    
    btn_reset=Button(frm,command=reset,text="reset",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_reset.place(relx=.53,rely=.3)
    
    btn_open=Button(frm,command=open_account,text="open account",width=16,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_open.place(relx=.4,rely=.42)
    
    btn_forgotpass=Button(frm,command=forgot_pass,width=19,text="forgot password",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_forgotpass.place(relx=.38,rely=.55)
    
def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.85)    
    
    def back():
        frm.destroy()
        main_screen()
     
    def send_otp():
        acn=entry_acn.get()
        email=entry_email.get()
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select email,password from accounts where acn=?",(acn,))
        row=cur.fetchone()
        if(row==None):
            messagebox.showerror("Password Recovery","ACN does not exist")
        else:
            if(row[0]==email):
                otp=random.randint(1000,9999)
                print(otp)
                try:
                    con=gmail.GMail("rahul8022raj@gmail.com","rrrf drbp irdh ipsx")
                    msg=gmail.Message(to=email,subject="OTP verification",text=f"You OTP is :{otp}")
                    con.send(msg)
                    messagebox.showinfo("Password Recovery","OTP sent,check your email")
                except:
                    messagebox.showerror("Password Recovery","Something went wrong")
                
                
                lbl_otp=Label(frm,text="otp",bg='pink',font=('arial',15,'bold'))
                lbl_otp.place(relx=.4,rely=.45)
    
                entry_otp=Entry(frm,font=('arial',20,'bold'),bd=5)
                entry_otp.place(relx=.4,rely=.5)
                entry_otp.focus()
                
                def getpass():
                    verify_otp=int(entry_otp.get())
                    if(otp==verify_otp):
                        messagebox.showinfo("Password Recovery",f"Your Pass:{row[1]}")
                    else:
                        messagebox.showerror("Password Recovery","Incorrect OTP")
                
                btn_verify=Button(frm,command=getpass,text="verify",font=('arial',20,'bold'),bd=5,bg='powder blue')
                btn_verify.place(relx=.6,rely=.6)
                
            else:
                messagebox.showerror("Password Recovery","Email is not correct")
        con.close()
        
    btn_back=Button(frm,command=back,text="Back",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_back.place(relx=0,rely=0)
    
    lbl_frmtitle=Label(frm,text="This is Forgot Password Screen",bg='pink',font=('arial',20,'bold'),fg='green')
    lbl_frmtitle.pack()

    lbl_acn=Label(frm,text="ACN",bg='pink',font=('arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.1)
    
    entry_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_acn.place(relx=.4,rely=.1)
    entry_acn.focus()
    
    lbl_email=Label(frm,text="Email",bg='pink',font=('arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.2)
    
    entry_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_email.place(relx=.4,rely=.2)
    
    btn_otp=Button(frm,command=send_otp,text="send OTP",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_otp.place(relx=.55,rely=.3)
    
def openaccount_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.85)    
    
    def back():
        frm.destroy()
        main_screen()
    
    def open_acn():
        name=entry_name.get()
        pwd=entry_pass.get()
        re_pwd=entry_re_pass.get()
        email=entry_email.get()
        mob=entry_mob.get()
        acn_type=combo_type.get()
        opendate=time.ctime()
        bal=1000

        if pwd==re_pwd:
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("insert into accounts(name,password,email,mob,bal,type,opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,acn_type,opendate))
            con.commit()
            con.close()
        
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select max(acn) from accounts")
            row=cur.fetchone()

            lbl_acn_open=Label(frm,text=f"Account opened with ACN:{row[0]}",bg='pink',font=('arial',20,'bold'),fg="green")
            lbl_acn_open.place(relx=.4,rely=.85)
            con.close()

        else:
            messagebox.showinfo("Pass Error!",message="Password doesn't match!")
     
    def reset():
        entry_name.delete(0,"end")
        entry_mob.delete(0,"end")
        entry_pass.delete(0,"end")
        entry_re_pass.delete(0,"end")
        entry_email.delete(0,"end")
        entry_name.focus()
        
        
    btn_back=Button(frm,command=back,text="Back",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_back.place(relx=0,rely=0)
    
    lbl_frmtitle=Label(frm,text="This is Open Account Screen",bg='pink',font=('arial',20,'bold'),fg='green')
    lbl_frmtitle.pack()
    
    lbl_name=Label(frm,text="Name",bg='pink',font=('arial',20,'bold'))
    lbl_name.place(relx=.3,rely=.1)
    
    entry_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_name.place(relx=.48,rely=.1)
    entry_name.focus()
    
    lbl_pass=Label(frm,text="Password",bg='pink',font=('arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.2)
    
    entry_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    entry_pass.place(relx=.48,rely=.2)

    lbl_re_pass=Label(frm,text="Re-type-Password",bg='pink',font=('arial',20,'bold'))
    lbl_re_pass.place(relx=.3,rely=.3)
    
    entry_re_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    entry_re_pass.place(relx=.48,rely=.3)
    
    lbl_email=Label(frm,text="Email",bg='pink',font=('arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.4)
    
    entry_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_email.place(relx=.48,rely=.4)
    
    lbl_mob=Label(frm,text="Mobile",bg='pink',font=('arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.5)
    
    entry_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_mob.place(relx=.48,rely=.5)
    
    lbl_type=Label(frm,text="Type",bg='pink',font=('arial',20,'bold'))
    lbl_type.place(relx=.3,rely=.6)
    
    combo_type=Combobox(frm,font=('arial',20,'bold'),values=['Saving','Current'])
    combo_type.current(0)
    combo_type.place(relx=.48,rely=.6)
    
    btn_open=Button(frm,command=open_acn,text="open",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_open.place(relx=.5,rely=.75)
    
    btn_reset=Button(frm,command=reset,text="reset",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_reset.place(relx=.6,rely=.75)
    
    
def loginaccount_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.85)    
    
    def logout():
        frm.destroy()
        main_screen()
    
    def details():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.55,relheight=.5)
        lbl_frmtitle.configure(text="This is Check Details Screen")
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn,bal,opendate,type from accounts where acn=?",(acn,))
        row=cur.fetchone()
        con.close()
        
        Label(ifrm,text=f"Account No.\t{row[0]}",font=('',15),bg='white',fg='purple').place(relx=.2,rely=.1)
        Label(ifrm,text=f"Account Bal\t{row[1]}",font=('',15),bg='white',fg='purple').place(relx=.2,rely=.2)
        Label(ifrm,text=f"Account opendate\t{row[2]}",font=('',15),bg='white',fg='purple').place(relx=.2,rely=.3)
        Label(ifrm,text=f"Account Type\t{row[3]}",font=('',15),bg='white',fg='purple').place(relx=.2,rely=.4)
    
    def update_profile():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.55,relheight=.5)
        lbl_frmtitle.configure(text="This is Update Profile Screen")
    
        def update_profile_afterlogin():
            name=entry_name.get()
            pwd=entry_pass.get()
            email=entry_email.get()
            mob=entry_mob.get()
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set name=?,password=?,email=?,mob=? where acn=?",(name,pwd,email,mob,acn,))
            con.commit()
            con.close()
            
            messagebox.showinfo("Update Profile","Profile Updated")
            lbl_wel.configure(text=f"Welcome,{name}")
            
        lbl_name=Label(ifrm,text="Name",bg='white',font=('arial',12,'bold'))
        lbl_name.place(relx=.1,rely=.1)
        
        entry_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_name.place(relx=.1,rely=.2)
        entry_name.focus()
        
        lbl_pass=Label(ifrm,text="Pass",bg='white',font=('arial',12,'bold'))
        lbl_pass.place(relx=.52,rely=.1)
        
        entry_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_pass.place(relx=.52,rely=.2)
        
        lbl_email=Label(ifrm,text="Email",bg='white',font=('arial',12,'bold'))
        lbl_email.place(relx=.1,rely=.4)
        
        entry_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_email.place(relx=.1,rely=.5)
        
        lbl_mob=Label(ifrm,text="Mob",bg='white',font=('arial',12,'bold'))
        lbl_mob.place(relx=.52,rely=.4)
        
        entry_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_mob.place(relx=.52,rely=.5)
        
        btn_update=Button(ifrm,command=update_profile_afterlogin,text="Update",font=('arial',15,'bold'),bd=5,bg='powderblue')
        btn_update.place(relx=.4,rely=.65)
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select name,password,email,mob from accounts where acn=?",(acn,))
        row=cur.fetchone()
        con.close()
        
        entry_name.insert(0,row[0])
        entry_pass.insert(0,row[1])
        entry_email.insert(0,row[2])
        entry_mob.insert(0,row[3])
        
        
        
        
        
    def deposit():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.55,relheight=.5)
        lbl_frmtitle.configure(text="This is Deposit Screen")
        
        def deposit_acn():
            amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select bal from accounts where acn=?",(acn,))
            bal=cur.fetchone()[0]
            cur.close()
            
            cur=con.cursor()
            cur.execute("update accounts set bal=bal+? where acn=?",(amt,acn))
            cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,amt,"Cr",time.ctime(),bal+amt))
            con.commit()
            con.close()
            
            messagebox.showinfo("Deposit",f"Amount {amt} credited to ACN:{acn}")
            
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        lbl_amt.place(relx=.1,rely=.2)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.3,rely=.2)
        entry_amt.focus()
        
        btn_dept=Button(ifrm,command=deposit_acn,text="deposit",font=('arial',20,'bold'),bd=5,bg='powderblue')
        btn_dept.place(relx=.4,rely=.4)
        
    
    def withdraw():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.55,relheight=.5)
        lbl_frmtitle.configure(text="This is Withdraw Screen")
    
        def withdraw_acn():
            amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select bal from accounts where acn=?",(acn,))
            bal=cur.fetchone()[0]
            cur.close()
            
            if(bal>amt):
                cur=con.cursor()
                cur.execute("update accounts set bal=bal-? where acn=?",(amt,acn))
                cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,amt,"Db",time.ctime(),bal-amt))
                con.commit()
                con.close()

                messagebox.showinfo("Withdraw",f"Amount {amt} withdrawn from ACN:{acn}")
            else:
                messagebox.showerror("Withdraw",f"Insufficient Bal:{bal}")
            
            
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        lbl_amt.place(relx=.1,rely=.2)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.3,rely=.2)
        entry_amt.focus()
        
        btn_widrw=Button(ifrm,command=withdraw_acn,text="withdraw",font=('arial',20,'bold'),bd=5,bg='powderblue')
        btn_widrw.place(relx=.4,rely=.4)
        
    def transfer():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.55,relheight=.5)
        lbl_frmtitle.configure(text="This is Transfer Screen")
        
        def transfer_acn():
            to_acn=entry_to.get()
            frm_amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select acn,bal from accounts where acn=?",(to_acn,))
            to_row=cur.fetchone()
            cur.close()
            if(to_row==None):
                messagebox.showerror("Transfer","To Account does not exist")
            else:    
                cur=con.cursor()
                cur.execute("select bal from accounts where acn=?",(acn,))
                bal=cur.fetchone()[0]
                cur.close()
                if(bal>frm_amt):
                    cur=con.cursor()
                    cur.execute("update accounts set bal=bal+? where acn=?",(frm_amt,to_acn))
                    cur.execute("update accounts set bal=bal-? where acn=?",(frm_amt,acn))
                    cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,frm_amt,"Db",time.ctime(),bal-frm_amt))
                    cur.execute("insert into txn_history values(?,?,?,?,?)",(to_acn,frm_amt,"Cr",time.ctime(),to_row[1]+frm_amt))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Transfer","Txn Done")
                else:
                    messagebox.showerror("Transfer",f"Insufficient Bal:{bal}")
            
        lbl_to=Label(ifrm,text="To",bg='white',font=('arial',20,'bold'))
        lbl_to.place(relx=.1,rely=.2)
        
        entry_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_to.place(relx=.3,rely=.2)
        entry_to.focus()
        
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        lbl_amt.place(relx=.1,rely=.4)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.3,rely=.4)
    
        
        btn_trans=Button(ifrm,command=transfer_acn,text="Transfer",font=('arial',20,'bold'),bd=5,bg='powderblue')
        btn_trans.place(relx=.4,rely=.6)
    
    def txn():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.55,relheight=.5)
        lbl_frmtitle.configure(text="This is Txn History Screen")
    
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,height=100,width=610)
        
        style = Style()
        style.configure("Treeview.Heading", font=('Arial',15,'bold'),foreground='black')

        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(x=600,y=0,height=100)
        tv.configure(yscrollcommand=sb.set)

        tv['columns']=('col1','col2','col3','col4')

        tv.column('col1',width=150,anchor='c')
        tv.column('col2',width=100,anchor='c')
        tv.column('col3',width=80,anchor='c')
        tv.column('col4',width=100,anchor='c')
        

        tv.heading('col1',text='Date')
        tv.heading('col2',text='Amt')
        tv.heading('col3',text='Type')
        tv.heading('col4',text='Updated Bal')

        tv['show']='headings'
        
        con=sqlite3.connect(database='banking.sqlite')
        cur=con.cursor()
        cur.execute("select * from txn_history where acn=?",(acn,))

        for row in cur:
            tv.insert("","end",values=(row[3],row[1],row[2],row[4]))

     
    def updatepic():
        img=filedialog.askopenfilename()
        shutil.copy(img,f"{acn}.png")
        img=Image.open(f"{acn}.png").resize((140,150))
        imgtk=ImageTk.PhotoImage(img,master=win)
        lbl_img.image=imgtk
        lbl_img['image']=imgtk
        
    btn_back=Button(frm,command=logout,text="logout",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_back.place(relx=.9,rely=0)
    
    lbl_frmtitle=Label(frm,text="This is Login Account Screen",bg='pink',font=('arial',20,'bold'),fg='green')
    lbl_frmtitle.pack()
    
    global lbl_wel
    lbl_wel=Label(frm,text=f"Welcome,{name}",bg='pink',font=('arial',20,'bold'),fg='green')
    lbl_wel.place(relx=0,rely=0)
    
    global img,imgtk,lbl_img
    if(os.path.exists(f"{acn}.png")):
        img=Image.open(f"{acn}.png").resize((140,150))
        imgtk=ImageTk.PhotoImage(img,master=win)
    else:
        img=Image.open("default.jpg").resize((140,150))
        imgtk=ImageTk.PhotoImage(img,master=win)
    
    lbl_img=Label(frm,image=imgtk)
    lbl_img.place(relx=.01,rely=.05)
    
    btn_propic=Button(frm,command=updatepic,text="update pic",bd=5,bg='powderblue')
    btn_propic.place(relx=.15,rely=.25)
    
    
    btn_details=Button(frm,command=details,width=12,text="Check details",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_details.place(relx=0,rely=.3)
    
    btn_update_profile=Button(frm,command=update_profile,width=12,text="Update Profile",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_update_profile.place(relx=0,rely=.4)
    
    btn_deposit=Button(frm,command=deposit,width=12,text="Deposit",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_deposit.place(relx=0,rely=.5)
    
    btn_withdraw=Button(frm,command=withdraw,width=12,text="Withdraw",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_withdraw.place(relx=0,rely=.6)
    
    btn_transfer=Button(frm,command=transfer,width=12,text="Transfer",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_transfer.place(relx=0,rely=.7)
    
    btn_txn=Button(frm,command=txn,width=12,text="Txn history",font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_txn.place(relx=0,rely=.8)
    
main_screen()
win.mainloop()



