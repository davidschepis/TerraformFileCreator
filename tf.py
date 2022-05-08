from re import sub
import sys
import os
import subprocess
import shutil

from pip import main
from DB.DB_Access import DB

def create_user(user):
    auth_user, id, _ = user
    username = ""
    password = ""
    print("Enter the desired username")
    username = input()
    print("Enter their password")
    password = input()
    create_user_result = DB.signup(username, password, auth_user)
    if create_user_result:
        print(f"User {username} successfully added under authorization of {auth_user}")
        main_screen(user)
    else:
        print("Unable to create user, returning to main screen")
        main_screen(user)
        
def list_users():
    users = DB.list_users()
    for i in users:
        username, id, auth = i
        print(f"Username: {username} ID: {id} Auth: {auth}")
        
def create_rg(user):
    #create folder
    os.mkdir("terraform-manifests")
    #create terraform block
    file = open("terraform-manifests/c1-version.tf", "x")
    file.write('terraform {\n\trequired_version=">=1.0.0"\n\trequired_providers {\n\t\tazurerm={\n\t\t\tsource="hashicorp/azurerm"\n\t\t\tversion=">=2.0"\n\t\t } \n\t } \n }\nprovider "azurerm" {\n\tfeatures{}\n}' + 
               '')
    #subprocess.run(["powershell", "cd terraform-manifests; terraform fmt"])
    #subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', '-l', "./ex.sh"])

def remove_tf_files(user):
    exists = os.path.isdir("terraform-manifests")
    if not exists:
        print("No folder terraform-manifests in current directory, returning to main screen")
        main_screen(user)
    else:
        try:
            shutil.rmtree("terraform-manifests")
            main_screen(user)
        except OSError as e:
            print(e)

def main_screen(user):
    user_input = -1
    while (user_input != 1 and user_input != 2 and user_input != 3):
        print("1. Create Resource Group")
        print("2. Add Authorized User")
        print("3. Show Users")
        print("4. Delete current Terraform files")
        print("5. Exit")
        try:
            user_input = int(input())
            break
        except ValueError:
            print("Please enter a 1, 2, or 3")
            continue
    if user_input == 5:
        exit()
    elif user_input == 3:
        list_users()
        main_screen(user)
    elif user_input == 2:
        create_user(user)
    elif user_input == 4:
        remove_tf_files(user)
    else:
        create_rg(user)
        

def start():
    args = str(sys.argv)
    if len(sys.argv) != 3:
        print("Usage python tf.py <username> <password>")
        exit()
    #login
    login_check = DB.login(sys.argv[1], sys.argv[2])
    if not login_check:
        print("Unable to login, please contact your database technician")
        exit()
    username, id, _ = login_check
    print(f"Welcome Username: {username} ID: {id}")
    main_screen(login_check)
start()