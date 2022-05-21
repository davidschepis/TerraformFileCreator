#! /bin/bash
cd ../kube-manifests
kubectl delete -f deployment.yaml
kubectl delete -f load-balancer.yaml
kubectl delete -f volume.yaml

