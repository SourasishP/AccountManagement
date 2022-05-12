import mysql.connector
import random
import re
import datetime
try:
    db_conn = mysql.connector.connect(host="localhost",user="test",password="test1234",database="online_manage")
    cur=db_conn.cursor()
except mysql.connector.errors.ProgrammingError:
    print("Not Connected")
    exit()
except:
    print("Something Went Wrong")
    exit()

def choose(acc_no,amt):
    print("\n\n1.Transact\n2.View Transactions\n3.Change Password\n4.Exit")
    ch=int(input("Enter Your Choice:"))
    if(ch==1):
        transact(acc_no,amt,1)
    elif(ch==2):
        view_transactions(acc_no,amt)
    elif(ch==3):
        change_password(acc_no)

def change_password(acc_no):
    print("Password must be of 8-10 characters, must have atleast one Uppercase, one Lowercase, one Digit and one Special Character")
    password_new=input("Enter your Password(Remember to keep this Password safe):")
    while(not re.match("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",password_new)):
        print("Password is not in requested format. Please enter it again:")
        password_new=input("")
    sqla="UPDATE users SET Password=%s,Acc_no_chg=%s WHERE Account_No=%s"
    value=(password_new,acc_no,acc_no)
    cur.execute(sqla,value)
    db_conn.commit()
    print("\nPassword Changed Successfully")
    login()
    
def view_transactions(acc_no,amt):
    j=0
    sql="SELECT Transaction_ID,To_acc_no,Amount,Date FROM transaction WHERE From_acc_no = %s"
    val=(acc_no,)
    cur.execute(sql,val)
    res=cur.fetchall()
    try:
        print("\t***Transaction Summary***")
        for i in res:
            print("Transaction ID:",res[j][0],"To Account No.:",res[j][1],"Amount:",res[j][2],"Date:",res[j][3])
            j=j+1
        print("\n\n")
        choose(acc_no,amt)
    except:
        print("No Transactions done until now")
        choose(acc_no,amt)
    
def transact(acc_no,amt,chk):
    tran_id=''
    if(chk==1):
        to_acc_no=input("Enter To Account Number:")
        sql="SELECT Email,Amount FROM users WHERE Account_No = %s"
        sql_acc_no=(to_acc_no,)
        cur.execute(sql,sql_acc_no)
        res=cur.fetchall()
        try:
            to_amt=float(res[0][1])
            send_amt=float(input("Enter Amount you want to send:"))
            if(send_amt<amt):
                deduct_amt=amt-send_amt
                to_amt=to_amt+send_amt
                for i in range(6):
                    tran_id=tran_id+str(random.randint(0,9))
                tran_id="ONL"+tran_id
                dt_tm=datetime.datetime.now()
                dt=str(dt_tm.year)+"-"+str(dt_tm.month)+"-"+str(dt_tm.day)
                sql="INSERT INTO transaction (Transaction_ID,To_acc_no,From_acc_no,Amount,Date) VALUES (%s,%s,%s,%s,%s)"
                value=(tran_id,to_acc_no,acc_no,send_amt,dt)
                cur.execute(sql,value)
                db_conn.commit()#Transaction Insertion
                sql="INSERT INTO performs (Transaction_ID,Acc_No_User) VALUES (%s,%s)"
                value=(tran_id,to_acc_no)
                cur.execute(sql,value)
                db_conn.commit()
                sql="UPDATE users SET Amount=%s WHERE Account_No=%s"
                value=(deduct_amt,acc_no)
                cur.execute(sql,value)
                db_conn.commit()
                sql="UPDATE users SET Amount=%s WHERE Account_No=%s"
                value=(to_amt,to_acc_no)
                cur.execute(sql,value)
                db_conn.commit()
                print("\t**Transaction Completed Successfully.\nYour Account has been debited with ",send_amt)
                print("Your New Balance is ",deduct_amt)
                choose(acc_no,amt)
            else:
                print("Send Amount Greater than Current Balance")
                choose(acc_no,amt)
        except:
            print("To Account Number is Invalid")
            choose(acc_no,amt)
    else:
        print("Please proceed for cash deposit of atleast 500")
        send_amt=500
        for i in range(6):
            tran_id=tran_id+str(random.randint(0,9))
        tran_id="ONL"+tran_id
        dt_tm=datetime.datetime.now()
        dt=str(dt_tm.year)+"-"+str(dt_tm.month)+"-"+str(dt_tm.day)
        sql="INSERT INTO transaction (Transaction_ID,To_acc_no,From_acc_no,Amount,Date) VALUES (%s,%s,%s,%s,%s)"
        value=(tran_id,"SELF",acc_no,send_amt,dt)
        cur.execute(sql,value)
        db_conn.commit()
        sql="INSERT INTO performs (Transaction_ID,Acc_No_User) VALUES (%s,%s)"
        value=(tran_id,acc_no)
        cur.execute(sql,value)
        db_conn.commit()
        sql="UPDATE users SET Amount=%s WHERE Account_No=%s"
        value=(send_amt,acc_no)
        cur.execute(sql,value)
        db_conn.commit()
        print("\t**Transaction Completed Successfully.\nYour Account has been credited with ",send_amt)
        print("Your New Balance is ",send_amt)

def registration():
    print("\n")
    nm=input("Enter your Name:")
    em=input("Enter your Email ID:")
    while(not re.match("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",em)):
        print("Invalid Email. Please enter it again:")
        em=input("")
    print("Password must be of 8-10 characters, must have atleast one Uppercase, one Lowercase, one Digit and one Special Character")
    password=input("Enter your Password(Remember to keep this Password safe):")
    while(not re.match("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",password)):
        print("Password is not in requested format. Please enter it again:")
        password=input("")
    uniq=input("Enter your Unique ID:")
    acc=""
    for i in range(10):
        acc=acc+str(random.randint(0,9))
    sql="INSERT INTO users (Name,Account_No,Aadhar,Email,Password,Amount) VALUES (%s,%s,%s,%s,%s,%s)"
    value=(nm,acc,uniq,em,password,0.0)
    cur.execute(sql,value)
    db_conn.commit()
    print("Registered Successfully\n")
    transact(acc,0,0)

def login():
    print("\n")
    em=input("Enter your Email ID:")
    paswd=input("Enter your Password:")
    sql="SELECT Email,Password,Account_No,Amount FROM users WHERE email = %s"
    em=(em,)
    cur.execute(sql,em)
    res=cur.fetchall()
    try:
        ch_paswd=res[0][1]
        acc_no=res[0][2]
        amt=res[0][3]
        if(ch_paswd==paswd):
            print("\t***Login In Successful***")
            choose(acc_no,amt)
        else:
            print("Invalid Password")
    except:
        print("Invalid Email ID")

a=0
while(a!=3):
    print("\t\t***Welcome to Online Banking System***")
    print("1.Registration\n2.Login\n3.Exit")
    a=int(input("Enter your Choice:"))
    if(a==1):
        registration()
    elif(a==2):
        login()
    elif(a==3):
        print("\t\t***Thank You***")
        print("\n")
