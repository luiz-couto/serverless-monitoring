#!/bin/bash

# create pyfile config map from handler.py
kubectl create configmap pyfile --from-file pyfile=src/handler.py --dry-run=client --output yaml > kube/pyfile.yaml

# create outputkey config map
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=luizcouto-proj3-output --dry-run=client  --output yaml > kube/outputkey.yaml

# apply the pyfile config map
kubectl apply -f kube/pyfile.yaml

# apply the outputkey config map
kubectl apply -f kube/outputkey.yaml

# apply deployment file
kubectl apply -f kube/deployment.yaml


