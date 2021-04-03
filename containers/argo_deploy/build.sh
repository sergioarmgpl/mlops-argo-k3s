#!/bin/bash
#Run as ./build.sh ARGOCD_DOMAIN ARGOCD_TOKEN DOCKERHUB_USER
docker login -u $3
docker build --build-arg argodomain=$1 --build-arg argotoken="$2" -t $3/argocd-deploy .
docker push $3/argocd-deploy

