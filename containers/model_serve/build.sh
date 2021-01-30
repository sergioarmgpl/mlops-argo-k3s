#!/bin/bash
docker login
docker build -t $1/sklearn_model_gcp .
docker push $1/sklearn_model_gcp
