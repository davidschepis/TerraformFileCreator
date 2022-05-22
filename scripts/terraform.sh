!/bin/bash
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

echo "Type yes to apply changes, anything else to quit"
read user_input
if [ "$user_input" = yes ]; then
    terraform apply -auto-approve >> history.txt
else
    echo "Terraform script ending"
fi