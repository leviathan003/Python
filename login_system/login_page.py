import string
import random
 
credentials=[]
check_dict = {}
users=[]
pwds=[]
username=''
pwd=''
pwd_base = list(string.ascii_letters+string.digits+"@!#,()'")

def gen_pwd(n):
    pwd=''
    for i in range(0,n):
        pwd+=random.choice(pwd_base)
    return pwd

def forgot_pwd(username):
    while username=='':
        print("Invalid Username!!!")
        username=input('Username: ')

    with open("login_system/credentials.txt","r") as file:
        for line in file:
            read_data = line.replace('\n','')
            credentials.append(read_data)
    for item in credentials:
            u_name=item.split('|')
            users.append(u_name[0])
           
    while username not in users:
        print("Username not Found.. If you are a new user then please sign in first")
        return '0'
    
    pwd_choice=input("Do you want to (a)Create own password (b)Use a suggested password: ")
        
    if pwd_choice=='a':
        new_pwd=input("Enter your password: ")
        while new_pwd=='':
            print("An empty password is like an open door...Anyone can come in..Please close the door")
            new_pwd=input("Enter new password: ")
    elif pwd_choice=='b':
        size=int(input("Input password length to generate password: "))
        new_pwd=gen_pwd(size)
        print("Your newly generated password is: ",new_pwd)

    index=users.index(username)
    credentials[index-1]=username+'|'+new_pwd

    with open("login_system/credentials.txt","w+") as file:
        for item in credentials:
            file.write(item+'\n')
    return new_pwd
    
        

def wrng_input(username,pwd):
    with open("login_system/credentials.txt","r") as file:
        for line in file:
            read_data = line.replace('\n','')
            credentials.append(read_data)

    for item in credentials:
        u_name,pwd_data=item.split('|')
        check_dict[u_name]=pwd_data
        users.append(u_name)

    while username not in users:
        print("Username not Found!!")
        username=input("Enter username: ")

    pwd=input("Enter password: ")
    while pwd != check_dict[username]:
        print("Error: Wrong Password!!")
        f_pwd=input("For forgot password enter(1), to retry press enter: ")
        if f_pwd=='1':
            credentials.clear()
            new_pwd=forgot_pwd(username)
            return username,new_pwd
        else:
            pwd=input("Enter password: ")
    return username,pwd   

def username_check(username):
    with open("login_system/credentials.txt","r") as file:
        for line in file:
            read_data = line.replace('\n','')
            credentials.append(read_data)
    for item in credentials:
            u_name=item.split('|')
            users.append(u_name[0])
    
    while username in users:
            print("Username Already Exists!! Please Choose another..")
            username=input("Enter your username: ").removesuffix(" ")     
    
    while username=='' or username==" ":
        print("Username cant be a Empty Field..Please enter a username")
        username=input("Username: ")

    return username


def pwd_check(pwd):
    with open("login_system/credentials.txt","r") as file:
        for line in file:
            read_data = line.replace('\n','')
            credentials.append(read_data)
    for item in credentials:
            u_name,passwd=item.split('|')
            pwds.append(passwd)
    if pwd in pwds:
        return 0
    else:
        return 1
    
def pwd_action(pwd_choice):
    if pwd_choice=='a':
        pwd=input("Enter your password(Please use atleast one Special character,eg:@,#,$,&): ")
        pass_checker=pwd_check(pwd)
        while pwd=='':
            print("An empty password is like an open door...Anyone can come in..Please close the door")
            pwd=input("Enter new password(Please use atleast one Special character,eg:@,#,$,&): ")
        while  pass_checker==0:
            print("The entered password is already in use..Please enter a different password..")
            pwd=input("Enter new password(Please use atleast one Special character,eg:@,#,$,&): ")
            pass_checker=pwd_check(pwd)
    elif pwd_choice=='b':
        size=int(input("Input password length to generate password: "))
        pwd=gen_pwd(size)
        pass_checker=pwd_check(pwd)
        while  pass_checker==0:
            pwd=gen_pwd(size)   
        print("Your generated password is: ",pwd)
    return pwd

def login_signup(mode):
    if mode ==1:
        username=input("Enter your username: ").removesuffix(" ")
        username=username_check(username)
        while username=='1':
            username=input("Enter your username: ").removesuffix(" ")
            username=username_check(username)
        pwd_choice=input("Do you want to (a)Create own password (b)Use a suggested password: ")
        while pwd_choice=="" or pwd_choice==" " or (pwd_choice!='a' and pwd_choice!='b') :
            print("Invalid Input!!")
            pwd_choice=input("Do you want to (a)Create own password (b)Use a suggested password: ")

        pwd=pwd_action(pwd_choice)
        
        with open("login_system/credentials.txt","a") as file:
            file.write(username+"|"+pwd+"\n")
        
    elif mode==2:
        print("Enter your username and password to login")
        username=input("Username: ")
        
        pwd='pwd'
        username,pwd=wrng_input(username,pwd)

        with open("login_system/credentials.txt","r") as file:
            for line in file:
                read_data = line.replace('\n','')
                credentials.append(read_data)
            
            data=username+'|'+pwd
    
            if data in credentials:
                print("Welcome ",username)
            else:
                print("Who are you, ",username)
    
    elif mode==3:
        username=input("Enter username: ")
        credentials.clear()
        pwd=forgot_pwd(username)
        while pwd=='':        
            username=input("Enter username: ")
            pwd=forgot_pwd(username)
        if pwd!='0':
            print("Password Changed Successfully!!")
    
    elif mode==4:
        print("\nQuitting Program...")
        exit(1)
    return
    
def main():
    with open('login_system/credentials.txt','w') as file:
        file.write('')
    while(True):
        print("\nWelcome to Python Login Page")
        print("Choose action:")
        print('1. Sign in(For new users)')
        print('2. Log in(For existing users)')
        print('3. Change Password')
        print('4. Quit Program')
        mode=int(input("mode: "))
        login_signup(mode)

main()