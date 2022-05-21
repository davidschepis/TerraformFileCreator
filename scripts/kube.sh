#! /bin/bash
echo "creating resource group"
az group create --name note-taker-rg --location centralus
sleep 1
echo "creating cluster"
az aks create -g note-taker-rg --node-count 1 --enable-managed-identity --node-vm-size standard_e2bds_v5 --vm-set-type VirtualMachineScaleSets --network-policy Azure --network-plugin azure --generate-ssh-keys --name note-taker-aks-server
sleep 1
echo "applying credentials"
az aks get-credentials --resource-group note-taker-rg --name note-taker-aks-server
