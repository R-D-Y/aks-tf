#!/bin/bash

# installs the NGINX Ingress controller on a K8s clutser

echo "Installing NGINX Ingress Controller..."

# Add the ingress-nginx repository to Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install the NGINX Ingress controller using Helm
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux

echo "NGINX Ingress Controller installey."
