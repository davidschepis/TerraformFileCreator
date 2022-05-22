import sys
import os
import subprocess
import shutil
import time

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
    
    #call bash script
    subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', '-l', "./scripts/terraform.sh"])
    #subprocess.run(["powershell", "cd terraform-manifests; terraform fmt"])
    main_screen(user)

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
            
def terraform_menu(user):
    user_input = -1
    while (user_input != 1 and user_input != 2 and user_input != 3):
        print("1. Create and run terraform files")
        print("2. Delete terraform files")
        print("3. Return to menu")
        try:
            user_input = int(input())
            break
        except ValueError:
            print("Please enter a a number (1-3)")
            continue
    if user_input == 1:
        create_rg(user)
    elif user_input == 2:
        remove_tf_files(user)
    else:
        main_screen(user)
        
def get_image_version():
    try:
        f = open("docker-current-version.txt", "r")
        version = f.read()
        version = int(version)
        f.close()
        return version
    except FileNotFoundError:
        print("Error! docker-current-version.txt not found, please create this file with the current version number")
        return -1
    finally:
        f.close()

def increment_version():
    try:
        version = get_image_version()
        if version == -1:
            return -1
        f = open("docker-current-version.txt", "w")
        version += 1
        f.write(str(version))
        f.close()
        return version
    except FileNotFoundError:
        print("Error! docker-current-version.txt not found, please create this file with the current version number")
        return -1
    except Exception as e:
        print(e)
        print("Please ensure docker-current-version.txt only contains a number which is the version number")
        return -1
        
def build_image(user):
    version = increment_version()
    if version == -1:
        docker_menu(user)
    rval = subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', f"./scripts/create_docker_image.sh", f"{version}"])
    if rval == 0:
        print("Image successfully built and published to Docker Hub! Returning to menu")
        docker_menu(user)
    else:
        print("Unable to create image, please check file system")
        docker_menu(user)
        
def start_local(user):
    version = get_image_version()
    rval = subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', "./scripts/docker_local_create.sh", f"{version}"])
    if rval == 0:
        print("Local instance started! url=localhost:3001")
        docker_menu(user)
    else:
        print("Unable to start local docker container")
        docker_menu(user)
        
def stop_local(user):
    rval = subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', "./scripts/docker_local_delete.sh"])
    if rval == 0:
        print("Local container stopped and removed")
        docker_menu(user)
    else:
        print("Unable to stop/remove local docker container")
        docker_menu(user)
       
def docker_menu(user):
    user_input = -1
    while (user_input != 1 and user_input != 2 and user_input != 3 and user_input != 4):
        print("1. Build/Publish Image")
        print("2. Start local instance on port 3001")
        print("3. Stop/Delete local instance")
        print("4. Return to menu")
        try:
            user_input = int(input())
            break
        except ValueError:
            print("Please enter a a number (1-3)")
            continue
    if user_input == 1:
        build_image(user)
    elif user_input == 2:
        start_local(user)
    elif user_input == 3:
        stop_local(user)
    else:
        main_screen(user)
        
def create_cluster(user):
    rval = subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', "./scripts/kube.sh"])
    if rval == 0:
        print("Cluster creation success, returning to menu")
        kubernetes_menu(user)
    else:
        print("Something went wrong")
        kubernetes_menu(user)
        
def create_deployment(user):
    rval = subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', "./scripts/create_deployment.sh"])
    if rval == 0:
        print("Deployment creating and running, returning to menu")
        kubernetes_menu(user)
    else:
        print("Something went wrong")
        kubernetes_menu(user)

def stop_deployment(user):
    rval = subprocess.call(['C:\\Program Files\\Git\\bin\\bash.exe', "./scripts/delete_deployment.sh"])
    if rval == 0:
        print("Deployment deleted, returning to menu")
        kubernetes_menu(user)
    else:
        print("Something went wrong")
        kubernetes_menu(user)
    
def kubernetes_menu(user):
    user_input = -1
    while (user_input != 1 and user_input != 2 and user_input != 3):
        print("1. Create Resource Group, Cluster, and apply credentials")
        print("2. Create and Start Deployment")
        print("3. Stop/Delete deployment")
        print("4. Return to menu")
        try:
            user_input = int(input())
            break
        except ValueError:
            print("Please enter a a number (1-3)")
            continue
    if user_input == 1:
        create_cluster(user)
    elif user_input == 2:
        create_deployment(user)
    elif user_input == 3:
        stop_deployment(user)
    else:
        main_screen(user)

def main_screen(user):
    user_input = -1
    while (user_input != 1 and user_input != 2 and user_input != 3 and user_input != 4 and user_input != 5 and user_input != 6):
        print("1. Terraform")
        print("2. Docker")
        print("3. Kubernetes")
        print("4. Add User")
        print("5. List Users")
        print("6. Exit")
        try:
            user_input = int(input())
            break
        except ValueError:
            print("Please enter a a number (1-6)")
            continue
    if user_input == 1:
        terraform_menu(user)
    elif user_input == 2:
        docker_menu(user)
    elif user_input == 3:
        kubernetes_menu(user)
    elif user_input == 4:
        create_user(user)
    elif user_input == 5:
        list_users()
        time.sleep(2)
        main_screen(user)
    else:
        print("Goodbye")
        time.sleep(1)
        exit()
        
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