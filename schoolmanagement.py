import mysql.connector as connection
import sys
import bcrypt

##### password check ##############

def encrypt(p):
    password_hash= bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt())
    password=password_hash.decode('utf-8')
    return password

def decrypt(store_p,user_p):
        if store_p:
            stored_password_hash = store_p[0].encode('utf-8')
            input_password_encoded = user_p.encode('utf-8')

            # Verify the input password against the stored hash
            if bcrypt.checkpw(input_password_encoded, stored_password_hash):
                return True
            else:
                return False
        else:
            return False


#### connection establish #################

def connct(query):
    mydb=connection.connect(host="localhost",root="root",password="root",database=data)
    curssor=mydb.cursor()
    curssor.execute(query)
########## create database ###############
class databs:
    def __init__(self):
        mydb=connection.connect(host="localhost",user="root",password="root")
        curssor=mydb.cursor()
        print("welecome to the data base system.......\n")
        global data
        data=input("enter the database name ->")
        self.dt=(data,)
        query="show databases"
        curssor.execute(query)
        result=curssor.fetchall()
        if self.dt in result:
            print("data base already exist")
            while True:
                ext=input("press 1 key for exit or press other key to continue")
                if ext=="1":
                    sys.exit()
                else:
                    try:
                        log=login()
                    except Exception as e:
                        print(e)
        else:
            query=f"create database {data}"
            curssor.execute(query)
            print("data base created sucessfully")
        try:
            mydb=connection.connect(host="localhost",user="root",password="root",database=data)
            curssor=mydb.cursor()
            query="show tables"
            curssor.execute(query)
            result=curssor.fetchall()
            if result!=[('login_info',), ('student_info',), ('teacher_info',)]:
                if "login_info" not in result:
                    query="create table login_info(username varchar(60) primary key ,password varchar(200),role varchar(20))"
                    curssor.execute(query)
                    print("login info table created sucessfully ")
                if "student_info" not in result:
                    query="create table student_info(student_id varchar(60),student_name varchar(20),mobile int(11),branch varchar(20),marks int(10))"
                    curssor.execute(query)
                    print("student info table created sucessfully ")
                if "teacher_info" not in result:
                    query="create table teacher_info(teacher_id varchar(60),teacher_name varchar(20),mobile int(11),department varchar(20),salary int(10))"
                    curssor.execute(query)
                    print("teacher info table created sucessfully ")
                else:
                    pass
                print("All the requirements are satisfied")
                account_create()
            else:
                print("All the requirements are satisfied  ")              
        except Exception as e:
            print(e)

#### login classs##################

class login():
    def __init__(self):
        print("ENTER YOUR LOGIN CREDENTIALS\n")
        self.username=input("user_name --> ")
        self.password=input("Password --> ")
        mydb=connection.connect(host="localhost",user="root",password="root",database=data)
        query="select username from login_info"
        curssor=mydb.cursor()
        curssor.execute(query)
        result=curssor.fetchall()
        if (self.username,) in result:
            query1=f"select password from login_info where username ='{self.username}'"
            curssor.execute(query1)
            result=curssor.fetchone()
            # s=decrypt(result,self.password)
            if decrypt(result,self.password) :
                query=f"select role from login_info where username='{self.username}'"
                curssor.execute(query)
                result=curssor.fetchall()
                if ('student',) in result:
                    query=f"select student_name from student_info where student_id='{self.username}'"
                    curssor.execute(query)
                    r=curssor.fetchall()
                    for i in r:
                        print(i,"   ","WELCOME")
                    while True:
                        n2=int(input("press 1 -> view details\npress 2 -> update mobile_number\npress 3 -> log out\n enter the key --> "))
                        if n2==1:
                            curssor.execute(f"select *from student_info where student_id='{self.username}'")
                            print(curssor.fetchall())
                        elif n2==2:
                            newp=input("enter mobile number - > ")
                            curssor=mydb.cursor()
                            curssor.execute(f"update student_info set mobile='{newp}' where student_id='{self.username}'")
                            mydb.commit()
                            print(" mobile updtaed ..........")
                        elif n2==3:
                            break
                        else:
                            print("chose the correct option")
                        
                elif ('admin',) in result:
                       print("Welcome back ", self.username)
                       while True:
                           n2=int(input("press 1 -> account create\npress 2 -> update account\npress 3 -> delete account\npress 4 ->view all details\npress 5 -> log out\n enter the key --> "))
                           if n2==1:
                               account_create()
                           elif n2==2:
                               curssor.execute("select username,role,password from login_info")
                               print(curssor.fetchall())
                               print("\n")
                               print("chose the option what to update ...\npress1 ->  Update password\npress -> 2 update role ")
                               a=int(input("enter your option "))
                               if a==1:
                                   a=input("enter the username ->  ")
                                   newp=input("new password- > ")
                                   newP=encrypt(newp)
                                   curssor=mydb.cursor()
                                   curssor.execute(f"update login_info set password='{newP}' where username='{a}'")
                                   mydb.commit()
                                   print("successfully updtaed ..........")
                               elif a==2:
                                    a=input("enter the username ->  ")
                                    newp=input("update role- > ")
                                    curssor=mydb.cursor()
                                    curssor.execute(f"update login_info set role='{newp}' where username='{a}'")
                                    mydb.commit()
                                    print("successfully updtaed ..........")
                               else:
                                   break           
                           elif n2==3:
                                a=input("enter the username for delete -> ")
                                curssor=mydb.cursor()
                                qw=curssor.execute(f"select role from login_info where username ='{a}'")
                                curssor.execute(f"delete from login_info where username ='{a}")
                                mydb.commit()
                                if ('student',) in qw:
                                    curssor.execute(f"delete from student_info where student_id='{a}'")
                                    mydb.commit()
                                elif ('teacher',) in qw:
                                    curssor.execute(f"delete from teacher_info where teacher_id='{a}'")
                                    mydb.commit()
                                print("sucessfully deleted .......")
                           elif n2==4:
                               query2="select username,role from login_info"
                               curssor.execute(query2)
                               print(curssor.fetchall())
                           else:
                               break
                        
                elif ('teacher',) in result:
                    query=f"select teacher_name from teacher_info where teacher_id='{self.username}'"
                    curssor.execute(query)
                    r=curssor.fetchall()
                    print(r)
                    for i in r:
                        print(i,"   ","WELCOME")
                    while True:
                        n2=int(input("press 1 -> all student details\npress 2 -> update marks\npress 3 -> view student\npress 4->log out\n enter the key --> "))
                        if n2==1:
                            curssor.execute("select *from student_info")
                            print(curssor.fetchall())
                        elif n2==2:
                            a=input("enter the username ->  ")
                            newp=input("update marks - > ")
                            curssor=mydb.cursor()
                            curssor.execute(f"update student_info set marks='{newp}' where student_id='{a}'")
                            mydb.commit()
                            print("marks  updtaed ..........")
                        elif n2==3:
                            a=input("enter the student name -> ")
                            curssor.execute(f"select *from student_info where student_name='{a}'")
                            print(curssor.fetchall())
                        elif n2==4:
                            break
                        else:
                            print("chose corect option")
                            
                else:
                    print("error 2")
            else:
                print("error 1")
        else:
            print("NO data found please check the password and username ")

            
########## ACCount create ################

class account_create:
    try:
        def __init__(self):
            self.role=input("enter the role -> ")
            self.username=input("enter user_name -> ")
            self.password=input("enter the password -> ")
            self.cnpassword=input("Re_enter Password ->  ")
            if self.cnpassword!=self.password:
                print("password missmatch\nplease renenter the password and user_name  -> ")
                account_create()
            else:
                try :
                    mydb=connection.connect(host="localhost",user="root",password="root",database=data)
                    pword=encrypt(self.password)
                    query="insert into login_info(username,password,role) values(%s,%s,%s)"
                    values=[(self.username),(pword),(self.role)]
                    curssor=mydb.cursor()
                    curssor.execute(query,values)
                    mydb.commit()
                except Exception as e :
                    # print("account already exist")
                    print(e)
                    # account_create()
                if self.role=="admin":
                    print("admin account succesfully created")
                elif self.role =="student":
                    self.stname=input("enter the student name -> \n")
                    self.branch=input("enter the student branch ->\n")
                    self.mobile=int(input("enter the mobile number -> \n"))
                    query="insert into student_info(student_id,student_name,mobile,branch) values(%s,%s,%s,%s)"
                    values=[(self.username),(self.stname),(self.mobile),(self.branch)]
                    curssor=mydb.cursor()
                    curssor.execute(query,values)
                    mydb.commit()
                    print(" student account succesfully created")
                elif self.role=="teacher":
                    self.tname=input("enter the teacher name -> \n")
                    self.department=input("enter the teacher department ->\n")
                    self.mobile=int(input("enter the mobile number -> \n"))
                    self.salary=int(input("enter the salary -> \n"))
                    query="insert into teacher_info(teacher_id,teacher_name,mobile,department,salary) values(%s,%s,%s,%s,%s)"
                    values=[(self.username),(self.tname),(self.mobile),(self.department),(self.salary)]
                    curssor=mydb.cursor()
                    curssor.execute(query,values)
                    mydb.commit()
                    print(" teacher account succesfully created")
                else:
                    print("ONLY ADMIN ,TEACHER , STUDENT ACCOUNT CAN BE MADE ")
    except Exception as e:
        print(e)
        


          
########## admin account create##########
class admin(databs):
    def __init__(self):
        ct=databs()
        mydb=connection.connect(host="localhost",user="root",password="root",database=data)
        query="select role from login_info"
        curssor=mydb.cursor()
        curssor.execute(query)
        result=curssor.fetchall()
        if ('admin',) in result:
            print("admin account already created ")
            print("press any key to continue or press 1 for exit")
            
            n=input("enter the number" )
            if n==1:
                sys.exit()
            else:
                try:
                    create=account_create()
                except Exception as e:
                    print(e)
        else:
            print("create the admin account")
            create=account_create()
            






######## main program ####################
databs()
while True:
    n=input("enter 1 to shutdown other key to continue")
    if n=='1':
        sys.exit()
    else:
        login()
        



