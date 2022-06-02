#!/bin/bash

terraform output -raw tls_private_key > id_rsa

terraform output public_ip_address

ssh -i id_rsa azureuser@<public_ip_address>