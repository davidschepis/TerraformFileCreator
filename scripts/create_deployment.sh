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
echo "Waiting for IP to be generated"
sleep 2
echo 10
sleep 2
echo 9
sleep 2
echo 8
sleep 2
echo 7
sleep 2
echo 6
sleep 2
echo 5
sleep 2
echo 4
sleep 2
echo 3
sleep 2
echo 2
sleep 2
echo 1
echo "Services written to services.json"
kubectl get svc -o json >> services.json
