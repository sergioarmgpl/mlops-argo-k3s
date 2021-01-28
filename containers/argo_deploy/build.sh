#!/bin/bash
#Run as ./build.sh ARGO_DOMAIN DOCKERHUB_USER
docker login
docker build --build-arg argodomain=$1 -t czdev/argocd-cli .
docker push $2/argocd-cli

