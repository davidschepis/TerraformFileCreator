#! /bin/bash
cd kube-manifests
kubectl apply -f deployment.yaml
kubectl apply -f load-balancer.yaml
kubectl apply -f volume.yaml
FILE=services.json
if test -f "$FILE"; then
    rm services.json
    echo "Removing old file"
fi
echo "Services written to services.json"
kubectl get svc -o json >> services.json
