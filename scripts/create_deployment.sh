#! /bin/bash
cd ../kube-manifests
kubectl apply -f deployment.yaml
kubectl apply -f load-balancer.yaml
kubectl apply -f volume.yaml
