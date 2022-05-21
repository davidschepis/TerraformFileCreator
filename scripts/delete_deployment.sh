#! /bin/bash
cd ../kube-manifests
kubectl delete -f rs.yaml
kubectl delete -f lb.yaml
kubectl delete -f pvc.yaml

