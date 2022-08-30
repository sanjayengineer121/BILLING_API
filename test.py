from flask import Flask, render_template,json,request,redirect,url_for
from flask_restful import Resource, Api
import json, string, random, os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import flask,requests
import webbrowser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import logging
import datetime
from datetime import date
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import platform
import socket
import sys
from sqlalchemy.sql.expression import select, exists

#==========================STARTING===================================

print(platform.node())
#app.config['UPLOAD_FOLDER'] = data/fileupload

#==========================DATE TIME===================================

now = datetime.datetime.now()

#==========================FLASK STARTER===================================

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sales.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(application)

#==========================DATABASE===================================

class TODO(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    Mobile=db.Column(db.Integer,nullable=False)
    Msg=db.Column(db.String(2000),nullable=False)
    date=db.Column(db.String(10),nullable=False)
    
    def to_dict(self):
        return {
            'sno': self.sno,
            'Mobile': self.Mobile,
            'Msg': self.Msg,
            'date': self.date
        }
    def __repr__(self) -> str:
        return f'{self.sno}'

#==========================DATABASE===================================

class Paymentsetup(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    bankacc=db.Column(db.String(50),nullable=False)
    Ifsccode=db.Column(db.String(20),nullable=False)
    Ownername=db.Column(db.String(50),nullable=False)
    UpiId=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(10),nullable=False)
    status = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'sno': self.sno,
            'bankacc': self.bankacc,
            'Ifsccode': self.Ifsccode,
            'Ownername':self.Ownername,
            'UpiId':self.UpiId,
            'date': self.date,
            'status':self.status
        }
    def __repr__(self) -> str:
        return f'{self.sno}'

#==========================DATABASE===================================

class Payment_Qr(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    Mobile=db.Column(db.Integer,nullable=False)
    PRICE=db.Column(db.Integer,nullable=False)
    customer_detailS=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(10),nullable=False)


    
    
    def to_dict(self):
        return {
            'sno': self.sno,
            'Mobile': self.Mobile,
            'PRICE': self.PRICE,
            'customer_detailS': self.customer_detailS,
            'date': self.date
        }
    def __repr__(self) -> str:
        return f'{self.sno}'

#==========================DATABASE VALIDATION===================================        

import os.path
file_exists = os.path.exists('sales.db')
if file_exists==1:
    pass
else:
    db.create_all()

#==========================MULTIPLE NUMBER===================================

file = open('data/number1.txt','r')  
with open("data/number1.txt") as mytxt:
    for line in mytxt:
        print (line)


#==========================CONFIG FILE READ===================================
 
with open('config.json','r') as openfile:
            port = json.load(openfile)
            port["port"]

#==========================MARG FILE READ===================================

with open('marg.json','r') as openfile:
            path1 = json.load(openfile)
            path1["path"]
            path1['method']
            print(path1['method'])

#==========================CREATE DATABSE CONNECTION===================================

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("sales.db")
        return conn
    except:
        print("error")

    return conn


    


#==========================CREATE SEND FILE AND ATTACHMENT===================================

@application.route("/send_att")
def demo_world():
    mobile = request.args.get('mobile')
    message = request.args.get('message')
    attach = request.args.get('attach')
    print(message)
    print(mobile)
    #webbrowser.open(attach)

    words = message.split()
    print(words)


    import json

    desc={
	 "lastbill":message
        }

    with open("data/lastbill.json", "w",encoding='utf-8') as outfile:

        json.dump(desc, outfile, ensure_ascii=False, indent=4)

    s=socket.gethostname()

    file = open('data/geek.txt','a')
    file.write("\n\n===============================================================================\n\n")
    file.write("======================================|mobile|=================================\n")
    file.write(mobile)
    file.write("\n====================================|SALES MSG|================================\n")
    file.write(message)
    file.write("\n======================================|DATE|===================================\n")
    file.write(str(now))
    file.write("\n\n===============================================================================\n\n")
    file.close()

    file = open('data/current.txt','w')
    file.write("\n\n===============================================================================\n\n")
    file.write("======================================|mobile|=================================\n")
    file.write(mobile)
    file.write("\n====================================|SALES MSG|================================\n")
    file.write(message)
    file.write("\n======================================|DATE|===================================\n")
    file.write(str(now))
    file.write("\n\n===============================================================================\n\n")
    file.close()

    

    if 'your total outstanding is' in message:
        print(words)
        sample=['Dear', 'x', 'y,', 'your', 'total', 'outstanding', 'is', 'Rs.1.00', 'Dr,Kindly', 'pay', 'as', 'earliest.', 'Sanjay', 'E', 'Shop']
        lis=[]
        for i in words:
            if i not in sample:
                lis.append(i)

        print(lis)
        
        for s in lis:
            if 'Rs' in s:
                amt=s[3:]
        
        print(amt)

        name=""

        for n in range(len(lis)-1):
            name=name+lis[n]+" "

        print(name)

        name=name.replace(",", "")

        from test import Paymentsetup
        from test import db
        #print(Paymentsetup.UpiId)

        import json

        with open('data/paymentdata.json','r') as openfile:
            path1 = json.load(openfile)
            path1["UPI ID"]

        UPI_ID=path1["UPI ID"]
        Payee_name=path1["Owner name"]
        Amount=amt.replace(",", "")
        Transaction_Note="Out Standing Amount of "+name
        Transaction_Ref_ID="s1"
        bankacc=path1["banka/c"]
        ifsc=path1["ifscNo"]

        UPI1="upi://pay?pa="+UPI_ID+"&pn="+Payee_name+"&am="+Amount+"&tr="+Transaction_Ref_ID+"&tn="+Transaction_Note
        UPI="upi://pay?pa="+UPI_ID+"&pn="+Payee_name+"&am="+Amount+"&tr=ss&tn="+Transaction_Note
        print(UPI)
        import qrcode
        qr = qrcode.make(UPI)
        s1=str(mobile)+'.png'
        s='data/paymentQr/'+str(mobile)+'.png'
        qr.save(s)
        import glob
        file = glob.glob('data/paymentQr/*') # * means all if need specific format then *.csv
        old = max(file, key=os.path.getctime)
        print(old)
        print(os.path.abspath(old))
        new=os.path.abspath(old)
        #webbrowser.open(new)

  
        sale1=Payment_Qr(Mobile=mobile,PRICE=Amount,customer_detailS=Payee_name,date=date.today())
        db.session.add(sale1)
        db.session.commit()
        url="https://freepay-upi.herokuapp.com/"+UPI_ID+"/"+Amount
        #message='kindly pay your payment of \n*'+Amount+'*\nand Acknowledge the reciept and pay by Qr code scan\n or can pay by clicking upi link \n'+url
        #Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+Mobile+"&message="+message+"&attach="+new
        #whatsAppHitApi = requests.get(Api)

        import pyshorteners

        long_url = "https://upiqr.codefind.in/upiqrview.php?name="+Payee_name+"&vpa="+bankacc+"@"+ifsc+".ifsc.npci&amt="+Amount
 
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(long_url)
 
        print("The Shortened URL is: " + short_url)


    
        

        if attach==None:
            Api="http://127.0.0.1:"+str(port["port"])+"/send?mobile="+mobile+"&message="+message
            whatsAppHitApi = requests.get(Api)
            with open("data/number1.txt") as line:
                    print (line)
                    Api="http://127.0.0.1:"+str(port["port"])+"/send?mobile="+line+"&message="+message
                    whatsAppHitApi = requests.get(Api)
        else:
            Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+mobile+"&message="+message+"&attach="+attach
            whatsAppHitApi = requests.get(Api)
            with open("data/number1.txt") as mytxt:
                for line in mytxt:
                    print (line)
                    Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+line+"&message="+message+"&attach="+attach
                    whatsAppHitApi = requests.get(Api)


        engine = create_engine('sqlite:///sales.db')
        Session = sessionmaker(bind=engine)
        import sqlalchemy
        
        session = Session()
        from test import TODO
        from test import db
        s1=session.query(exists().where(TODO.Mobile==mobile,TODO.Msg==message)).scalar()

    #==========================CHECKING DUPLICATE ENTRY===================================
        
        if s1==1:
            todo = TODO.query.filter_by(Msg=message,Mobile=mobile).first()
            todo.date = date.today()
            db.session.commit()
            return "updated"

            


        else:
            #sale=TODO(Mobile=mobile,Msg=message,date=date.today())
            #db.session.add(sale)
            #db.session.commit() 
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO TODO (Mobile,Msg,date) VALUES ( '"+mobile+"', '"+message+"','"+str(date.today()) +"')")
            conn.commit()   
            COMMASPACE = ', '

       
            if __name__ == '__main__':
                demo_world()
            
            return "HELLO"

#==========================send without attachment tally===================================

@application.route("/send")
def demo():
    mobile = request.args.get('mobile')
    message = request.args.get('message')
    print(message)
    print(mobile)
    #webbrowser.open(attach)
    import json

    desc={
	 "lastbill":message
        }

    with open("data/lastbill.json", "w",encoding='utf-8') as outfile:

        json.dump(desc, outfile, ensure_ascii=False, indent=4)

    words = message.split()
    print(words)


    file = open('data/geek.txt','a')
    file.write("\n\n===============================================================================\n\n")
    file.write("======================================|mobile|=================================\n")
    file.write(mobile)
    file.write("\n====================================|SALES MSG|================================\n")
    file.write(message)
    file.write("\n======================================|DATE|===================================\n")
    file.write(str(now))
    file.write("\n\n===============================================================================\n\n")
    file.close()

    file = open('data/current.txt','w')
    file.write("\n\n===============================================================================\n\n")
    file.write("======================================|mobile|=================================\n")
    file.write(mobile)
    file.write("\n====================================|SALES MSG|================================\n")
    file.write(message)
    file.write("\n======================================|DATE|===================================\n")
    file.write(str(now))
    file.write("\n\n===============================================================================\n\n")
    file.close()

    

    s=socket.gethostname()
    print(s)
    IP_addres = socket.gethostbyname(s)

    Api="http://127.0.0.1:"+str(port["port"])+"/send?mobile="+mobile+"&message="+message
    whatsAppHitApi = requests.get(Api)
    with open("data/number1.txt") as mytxt:
        for line in mytxt:
            print (line)
            Api="http://127.0.0.1:"+str(port["port"])+"/send?mobile="+line+"&message="+message
            whatsAppHitApi = requests.get(Api)
    
    #Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+line1+"&message="+message+"&attach="+attach
    #whatsAppHitApi = requests.get(Api)

#==========================creating db connection===================================


    engine = create_engine('sqlite:///sales.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    from test import TODO
    from test import db
    s1=session.query(exists().where(TODO.Mobile==mobile,TODO.Msg==message)).scalar()

    if s1==1:
        #s=session.query(exists().where(TODO.Msg==message and TODO.Mobile==mobile)).scalar()

        todo = TODO.query.filter_by(Msg=message,Mobile=mobile).first()
        todo.date = date.today()
        db.session.commit()

        return "updated"

    else:
        sale=TODO(Mobile=mobile,Msg=message,date=date.today())
        db.session.add(sale)
        db.session.commit()       
        COMMASPACE = ', '

        if session.query(exists().where(Email_data.status==1)).scalar()==1:
            def main():
                sender = 'sanjay.yadav@ensowt.com'
                gmail_password = 'sanjZ1234@'
                recipients = ['sanjayyadav7071@gmail.com']
                

                outer = MIMEMultipart()
                outer['Subject'] = message
                outer['To'] = COMMASPACE.join(recipients)
                outer['From'] = sender
                outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
                

                
                # Python code to illustrate Sending mail from
                # your Gmail account
                import smtplib

                # creates SMTP session
                s = smtplib.SMTP('smtp.gmail.com', 587)

                # start TLS for security
                s.starttls()

                # Authentication
                s.login(sender, gmail_password)

                # message to be sent
                message1 = "Dear Sir/Madam\n"+message+"\n thanks for purchasing with Us\nSanjay E shop Ph. 6388574919"
                print(message1) 

                # sending the mail
                s.sendmail(sender, recipients , message1)
                print("mail sent")

                # terminating the session
                s.quit()

        if __name__ == '__main__':
            demo()        
        
        return "HELLO"

#==========================Marg erp Billing data===================================


@application.route("/margerp")
def demo_world1():
    s=socket.gethostname()
    print(s)
    IP_addres = socket.gethostbyname(s)
    mobile = request.args.get('mobile')
    message = request.args.get('message')
    print('============================================================\n')
    print(mobile)
    print('============================================================\n')
    print(message)

    #webbrowser.open(latest_file)
   

    words = message.split()
    
    
    file = open('data/geek.txt','a')
    file.write("\n\n===============================================================================\n\n")
    file.write("======================================|mobile|=================================\n")
    file.write(mobile)
    file.write("\n====================================|SALES MSG|================================\n")
    file.write(message)
    file.write("\n======================================|DATE|===================================\n")
    file.write(str(now))
    file.write("\n\n===============================================================================\n\n")
    file.close()

    file = open('data/current.txt','w')
    file.write("\n\n===============================================================================\n\n")
    file.write("======================================|mobile|=================================\n")
    file.write(mobile)
    file.write("\n====================================|SALES MSG|================================\n")
    file.write(message)
    file.write("\n======================================|DATE|===================================\n")
    file.write(str(now))
    file.write("\n\n===============================================================================\n\n")
    file.close()
    welcome ="Thanks for shoping" 
    import glob
    list_of_files = glob.glob(path1["path"]+'emailserver/*') # * means all if need specific format then *.csv
    latest_file1 = max(list_of_files, key=os.path.getctime)
    print(latest_file1)

    import shutil
    shutil.copy(latest_file1, 'data/attach/')
    file = glob.glob('data/attach/*') # * means all if need specific format then *.csv
    old = max(file, key=os.path.getctime)
    print(old)
    print(os.path.abspath(old))
    new=os.path.abspath(old)
    Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+mobile+"&message="+message+"&attach="+new
    whatsAppHitApi = requests.get(Api)
    with open("data/number1.txt") as mytxt:
        for line in mytxt:
            print (line)
            Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+line+"&message="+message+"&attach="+new
            whatsAppHitApi = requests.get(Api)
    
    engine = create_engine('sqlite:///sales.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    from test import TODO
    from test import db

    s1=session.query(exists().where(TODO.Mobile==mobile,TODO.Msg==message)).scalar()

    if s1==1:
        todo = TODO.query.filter_by(Msg=message,Mobile=mobile).first()
        todo.date = date.today()
        db.session.commit()
        print("Database already exist")

    else:
         
        sale=TODO(Mobile=mobile,Msg=message,date=date.today())
        db.session.add(sale)
        db.session.commit()       

        COMMASPACE = ', '
        def main():

            sender = 'sanjay.yadav@ensowt.com'
            gmail_password = 'sanjZ1234@'
            recipients = ['sanjayyadav7071@gmail.com']
            
            # Create the enclosing (outer) message
            outer = MIMEMultipart()
            outer['Subject'] = mobile
            outer['To'] = COMMASPACE.join(recipients)
            outer['From'] = sender
            outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            # List of attachments
            attachments = [new]

            # Add the attachments to the message
            for file in attachments:
                try:
                    with open(file, 'rb') as fp:
                        msg = MIMEBase('application', "octet-stream")
                        msg.set_payload(fp.read())
                    encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    outer.attach(msg)
                except:
                    print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                    raise

            composed = outer.as_string()

            # Send the email
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as s:
                    s.ehlo()
                    s.starttls()
                    s.ehlo()
                    s.login(sender, gmail_password)
                    s.sendmail(sender, recipients, composed)
                    s.close()
                print("Email sent!")
            except:
                print("Unable to send the email. Error:")
                raise

        if __name__ == '__main__':
            demo_world1()       

    return "HELLO"

#==========================GET LAST MESSAGE===================================
import jsonify

def current_msg():
    with open('data/lastbill.json', 'r') as openfile:
                    lastbill = json.load(openfile)
    print([lastbill["lastbill"]])
    return jsonify(request.json)
#====================================Email Data Addition================================

@application.route("/PAYSETUP", methods = ['GET', 'POST'])
def PAYSETUP():
    bank= request.form.get("bank")
    print(bank)
    ifsc = request.form.get("ifsc")
    print(ifsc)
    payee=request.form.get("payee")
    print(payee)
    upiid = request.form.get("upiid")
    print(upiid)
    import json

    desc={
	 "banka/c":bank,
	 "ifscNo": ifsc,
     "Owner name": payee,
     "UPI ID": upiid,
        }

    with open("data/paymentdata.json", "w",encoding='utf-8') as outfile:

        json.dump(desc, outfile, ensure_ascii=False, indent=4)


        
#====================================PAYMENT DATA Addition to db================================

    paydata=Paymentsetup(bankacc=bank,Ifsccode=ifsc,Ownername=payee,UpiId=upiid,date=date.today(),status=False)
    db.session.add(paydata)
    db.session.commit()
    return redirect(url_for("index"))

@application.route("/update/<int:bankac>")
def update(bankac):
    payment = Paymentsetup.query.filter_by(sno=bankac).first()
    payment.status = not payment.status
    db.session.commit()
    return redirect(url_for("paysetup"))

#====================================Whatsapp pramotion================================

@application.route("/pramote", methods = ['GET', 'POST'])
def pramote():
    message = request.form.get("message")
    print(message)
    file = request.files['file']
    filename = flask.Request.full_path(file)
    print(filename)


    import subprocess
    subprocess.Popen(["notepad","data/number1.txt"])
    line='6388574919'
    Api="http://127.0.0.1:8086"+"/send_att?mobile="+line+"&message="+message+"&attach="+new_path
    whatsAppHitApi = requests.get(Api)

    return "success"



    return "successfully send"
#====================================Sales Msg Configuration================================

@application.route("/salesmsg", methods = ['GET', 'POST'])
def salesmsg():
    return render_template("salemsg.html",)



    return "successfully send"
#====================================Whatsapp qr Generate================================
    
@application.route("/whatsapp", methods = ['POST', 'GET'])
def whatsappQR():
    return render_template("QRCODE.html")
    

#====================================Whatsapp qr Generate================================

@application.route("/GENQR", methods=["POST"])
def add():
    Mobile = request.form.get("Mobile")
    Message = request.form.get("Message")
    print(Mobile)
    print(Message)
    import qrcode
    #https://wa.me/919818428221?text=Hi

    from flask_qrcode import QRcode
    #QRcode(application)

    #app.register_blueprint(bp)
    
    qrdata="https://wa.me/91"+Mobile+"?text="+Message

    sale=whatsappQr(Mobile=Mobile,MESSAGE=Message,date=date.today())
    db.session.add(sale)
    db.session.commit()
    
    #webbrowser.open('wrcode.png')


    #shutil.copy('wrcode.png', 'data/whatsappQr/')
    #file = glob.glob('data/whatsappQr/*') # * means all if need specific format then *.csv
    #old = max(file, key=os.path.getctime)
    #print(old)
    #print(os.path.abspath(old))
    #new=os.path.abspath(old)
    
    #return flask.send_file('wrcode.png', mimetype='image/png')


    return redirect(url_for("whatsappQR"))


#====================================Payment qr Generate================================

@application.route("/payment",methods = ['GET', 'POST'])
def pay():

    return render_template('index.html')

@application.route("/upi",methods = ['GET', 'POST'])
def pay1():

    return render_template('upi.html')

@application.route("/paymentbank",methods = ['GET', 'POST'])
def paybank():

    return render_template('bankpay.html')

@application.route("/upiqr", methods=["POST"])
def upi():
    import qrcode
    Mobile = request.form.get("mobile")
    print(Mobile)
    UPI_ID = request.form.get("pa")
    print(UPI_ID)
    Payee_name = request.form.get("pn")
    print(Payee_name)
    Amount = request.form.get("am")
    print(Amount)
    Transaction_Ref_ID = request.form.get("tr")
    print(Transaction_Ref_ID)
    Transaction_Note = request.form.get("tn")
    print(Transaction_Note)

    UPI="upi://pay?pa="+UPI_ID+"&pn="+Payee_name+"&am="+Amount+"&tr="+Transaction_Ref_ID+"&tn="+Transaction_Note

    qr = qrcode.make(UPI)
    s1=str(Mobile)+'.png'
    s='data/paymentQr/'+str(Mobile)+'.png'
    qr.save(s)
    import glob
    file = glob.glob('data/paymentQr/*') # * means all if need specific format then *.csv
    old = max(file, key=os.path.getctime)
    print(old)
    print(os.path.abspath(old))
    new=os.path.abspath(old)
    webbrowser.open(new)

    conn = create_connection()

    sale1=Payment_Qr(Mobile=Mobile,PRICE=Amount,customer_detailS=Payee_name,date=date.today())
    db.session.add(sale1)
    db.session.commit()
    url="https://freepay-upi.herokuapp.com/"+UPI_ID+"/"+Amount
    message='kindly pay your payment of \n*'+Amount+'*\nand Acknowledge the reciept and pay by Qr code scan\n or can pay by clicking upi link \n'+url
    Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+Mobile+"&message="+message+"&attach="+new
    whatsAppHitApi = requests.get(Api)

    x="qr code has been sent to\n"+Mobile+"\nand you can pay through Link as well"

    return x

@application.route("/bankpay", methods=["POST"])
def bankpay():
    import qrcode
    Name = request.form.get("hname")
    print(Name)
    Account_no = request.form.get("acno")
    print(Account_no)
    IFSCCODE = request.form.get("ifsc")
    print(IFSCCODE)
    Amount = request.form.get("amt")
    print(Amount)

    bankpay1="https://upiqr.codefind.in/upiqrview.php?name="+Name+"&vpa="+Account_no+"@"+IFSCCODE+".ifsc.npci&amt="+Amount
    bankpay="upi://pay?pa="+Account_no+"@"+IFSCCODE+".ifsc.npci&pn="+Name+"&am="+Amount+"&tn=hello&cu=INR"


    qr = qrcode.make(bankpay)
    s1=str(Account_no)+'.png'
    s='data/paymentQr/'+str(Account_no)+'.png'
    qr.save(s)
    import glob
    file = glob.glob('data/paymentQr/*') # * means all if need specific format then *.csv
    old = max(file, key=os.path.getctime)
    print(old)
    print(os.path.abspath(old))
    new=os.path.abspath(old)
    webbrowser.open(new)

    conn = create_connection()

    #sale1=Payment_Qr(Mobile=Mobile,PRICE=Amount,customer_detailS=Payee_name,date=date.today())
    #db.session.add(sale1)
    #db.session.commit()
    #url="https://freepay-upi.herokuapp.com/"+UPI_ID+"/"+Amount
    #message='kindly pay your payment of \n*'+Amount+'*\nand Acknowledge the reciept and pay by Qr code scan\n or can pay by clicking upi link \n'+url
    #Api="http://127.0.0.1:"+str(port["port"])+"/send_att?mobile="+Mobile+"&message="+message+"&attach="+new
    #whatsAppHitApi = requests.get(Api)





@application.route("/current", methods = ['GET', 'POST'])
def home():
    
    return flask.send_file("data/current.txt")


@application.route("/upload", methods = ['GET', 'POST'])
def upload():
    import json
    import requests
    headers = {"Authorization": "Bearer ya29.A0AVA9y1ti5VbU3ap353kxYp_Z0P9Nr3pUiKFujWP3u_YW9QtmK2zPYnCHAdl9hV-W-IBILiVVbi7hOojUKn7ADwaYKWTdhEzUDjaFTiTSs8N3fD5ihGRyIy2oAxYwZZSYTHQNnQtlM_mznsbMe5y6J0G19KVrYUNnWUtBVEFTQVRBU0ZRRTY1ZHI4Vk1mbzZ6ZmNuNkdkN19VdWE3T19UUQ0163"}
    para = {
        "name": "sales.db",
        "parents":["1EExGM3Z83KJ2JBXly54cYbJMlZKf2kXD"]
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("./sales.db", "rb")
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    print(r.text)
    
    return "Uploaded"

@application.route('/sales', methods = ['GET', 'POST'])
def uploader():
    return flask.send_file("data/geek.txt")


@application.route('/', methods = ['GET', 'POST'])
def index():
    DATA = TODO.query.all()
    return render_template('data.html', title='Data-Table',DATA = DATA,TODO=TODO)

@application.route('/data', methods = ['GET', 'POST'])
def transaction():
    DATA = TODO.query.all()
    return render_template('TRANSACTION.html', title='Data-Table',DATA = DATA,TODO=TODO)


@application.route('/paysetup', methods = ['GET', 'POST'])
def paysetup():
    Paymentdata = Paymentsetup.query.all()
    return render_template('paysetup.html',Paymentdata=Paymentdata,Paymentsetup=Paymentsetup)

@application.route('/pramotion', methods = ['GET', 'POST'])
def pramotion():
    return render_template('pramotion.html')




@application.route('/api/data')
def data():
    query = TODO.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            TODO.sno.like(f'%{search}%'),
            TODO.Mobile.like(f'%{search}%'),
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['sno', 'Mobile']:
            col_name = 'Mobile'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(TODO, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [todo.to_dict() for todo in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': TODO.query.count(),
        'draw': request.args.get('draw', type=int),
    }

    
if __name__ == '__main__':
    application.debug = True
    url="http://127.0.0.1:"+str(8086)+"/"
    webbrowser.open_new(url)
    application.run(host="0.0.0.0",port=8086)
    #webbrowser.open_new(url)
    