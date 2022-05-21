az group create --name note-taker-rg --location centralus
az aks create -g note-taker-rg --node-count 1 --enable-managed-identity --node-vm-size standard_e2bds_v5 --vm-set-type VirtualMachineScaleSets --network-policy Azure --network-plugin azure --generate-ssh-keys --name note-taker-aks-server
az aks get-credentials --resource-group note-taker-rg --name note-taker-aks-server
kubectl apply -f rs.yaml
kubectl apply -f lb.yaml