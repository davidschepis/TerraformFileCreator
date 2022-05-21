#! /bin/bash
cd ../kube-manifests
kubectl apply -f rs.yaml
kubectl apply -f lb.yaml
kubectl apply -f pvc.yaml
