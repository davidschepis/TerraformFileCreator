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
    #create resource group
    file = open("terraform-manifests/c2-resource-group.tf", "x")
    file.write('resource "azurerm_resource_group" "rg-1" {\n\tname = "rg-1"\n\tlocation="East US"\n}')
    #create VNET
    file = open("terraform-manifests/c3-virtual-network.tf", "x")
    vnet_text = 'resource "azurerm_virtual_network" "vnet" {'
    vnet_text += '\n\tname = "vnet-1"'
    vnet_text += '\n\taddress_space = ["10.0.0.0/16"]'
    vnet_text += '\n\tlocation = azurerm_resource_group.rg-1.location'
    vnet_text += '\n\tresource_group_name = azurerm_resource_group.rg-1.name'
    vnet_text += '\n\ttags = {\n\t\t"Env" = "Dev"\n\t}\n}\n'
    subnet_text = 'resource "azurerm_subnet" "subnet" {\n'
    subnet_text += '\tname = "subnet"\n'
    subnet_text += '\tresource_group_name = azurerm_resource_group.rg-1.name\n'
    subnet_text += '\tvirtual_network_name = azurerm_virtual_network.vnet.name\n'
    subnet_text += '\taddress_prefixes = ["10.0.2.0/24"]\n}\n'
    ip_text = 'resource "azurerm_public_ip" "publicip" {\n'
    ip_text += '\tname = "publicip"\n'
    ip_text += '\tresource_group_name = azurerm_resource_group.rg-1.name\n'
    ip_text += '\tlocation = azurerm_resource_group.rg-1.location\n'
    ip_text += '\tallocation_method = "Static"\n'
    ip_text += '\ttags = {\n\t\tenvironment = "Dev"\n\t}\n}\n'
    neti_text = 'resource "azurerm_network_interface" "vmnic" {\n'
    neti_text += '\tname = "vmnic"\n'
    neti_text += '\tlocation = azurerm_resource_group.rg-1.location\n'
    neti_text += '\tresource_group_name = azurerm_resource_group.rg-1.name\n'
    neti_text += '\tip_configuration {\n'
    neti_text += '\t\tname = "internal"\n'
    neti_text += '\t\tsubnet_id = azurerm_subnet.subnet.id\n'
    neti_text += '\t\tprivate_ip_address_allocation = "Dynamic"\n'
    neti_text += '\t\tpublic_ip_address_id = azurerm_public_ip.publicip.id\n\t}\n}'
    file.write(vnet_text + subnet_text + ip_text + neti_text)
    
    subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', '-l', "./ex.sh"])
    #subprocess.run(["powershell", "cd terraform-manifests; terraform fmt"])
    

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