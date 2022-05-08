#!/bin/bash -xv
echo "Changing into directory"
sleep 1
cd terraform-manifests
sleep 1
echo "Creating history file"
touch history.txt
sleep 1
terraform fmt
echo "Formatting Terraform files"
sleep 1
terraform init >> history.txt
echo "Initiating Terraform"
sleep 1
terraform validate >> history.txt
echo "Validating Terraform files"
sleep 1
terraform plan >> history.txt
echo "Planning Terraform files"
