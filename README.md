# MLOPS USING ARGO & K3S
This repo explains how to use Argo and K3s to automate Machine Learning pipelines called MLOps.

# PREREQUISITES
- Create a Virtual Machine on your prefered cloud provide
    - Suggested size 2 CPUs + 4GB Ram
    - Suggested OS Ubuntu 20.04 LTS
    - Check that all ports are opened
    - Set a static Public IP for your VM
- A Domain Name configured (ex. mlops.tk)
    - Point your domain to the public ip of your VM

## K3s installation
The following commands have to be executed inside your virtual machine:
1. First update your Ubunut
```
sudo apt-get update
```
2. Set a variable with your Public IP
```
PUBLIC_IP=YOUR_IP
```
3. Install k3s with the next command
```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --tls-san "$PUBLIC_IP" --node-external-ip "$PUBLIC_IP" --write-kubeconfig-mode 644" sh -s -
```
4. Check that your unique node is on Ready status, with the next command
```
kubectl get nodes
```
5. Install helm with the following commands
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
6. Download the kubeconfig in your local machine
```
ssh -i id_rsa yourUser@yourDomain cat /etc/rancher/k3s/k3s.yaml > ~/.kube/config
```
7. Change the Kubernetes API connection from:  
server: https://127.0.0.1:6443  
to  
server: https://yourDomain:6443  

## Nginx ingress controller Installation
This section is to install NGINX as ingress controller, to install it follow the next steps:
1. Create a namespace for NGINX
```
kubectl create ns ingress-nginx
```
2. Add the NGINX Helm repo
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx 
helm repo update
```
3. Install NGINX inside the ingress-nginx namespace
```
helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx
```

## Argo Workflows Installation
This section install Argo Workflows, follow the next for this:
1. Create a namespace called argo to install Argo Workflows
```
kubectl create ns argo
```
2. Install Argo Workflows using kubectl
```
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml
```
3. Because you are using k3s you have to support containerd as the container runtime with the next command:
```
kubectl patch configmap/workflow-controller-configmap \
-n argo \
--type merge \
-p '{"data":{"containerRuntimeExecutor":"k8sapi"}}'
```
4. Check that everything is running with the next command:
```
kubectl get pods -n argo
```
5. Access your Argo Workflow Deployment with port forward:
```
kubectl -n argo port-forward svc/argo-server 2746:2746
```
6. Access Argo Workflow on your browser accessing the next url:
```
http://127.0.0.1:2746
```
Note: If you are using port-forward to access Argo Workflows locally,  allow insecure connections from localhost in your browser. In Chrome, browse to: chrome://flags/. Search for “insecure” and you should see the option to “Allow invalid certificates for resources loaded from localhost.” Enable that option and restart your browser. Remember that by defaul Argo Workflows is installed with TLS.



## ArgoCD Installation
This section is to install ArgoCD with the next commands:
1. Create a namespace for ArgoCD:
```
kubectl create namespace argocd
```
2. Install ArgoCD using kubectl
```
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
3. Create the ingress controller modifing the file inside the argocd folder called argocd-ingress.yaml with your desired domain, for that check the host and hosts sections inside the file, then apply the YAML file with the next command:
```
kubectl apply -f argocd/argocd-ingress.yaml
```
4. Set an A DNS record pointing to the subdomain where ArgoCD will be accesible
Note: Because this is one node Kubernetes, the IP of the node is the same IP for the Load Balancer

### ArgoCD Password
1. To get the ArgoCD password and generate a Token to launch ArgoCD get the argocd-server pod name, this will be the password to access ArgoCD, execute the next line to get argocd-server pod name:
```
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2
```
2. Set a variable with the domain where ArgoCD is accesible
```
ARGOCD_SERVER=YourDomain
```
3. Generate the token to access the ArgoCD API, this is necessary to call ArgoCD when Argo Workflow need it
```
curl -sSL -k $ARGOCD_SERVER/api/v1/session -d $'{"username":"admin","password":"argocd-server-XXX-YYY"}'
```
Note: The password is the name of your argocd pod inside your argocd namespace


## Create bucket to upload information
For this repo is used Google Cloud Storage for the buckets, but you can use the Cloud Provider of your choice.
For Google Cloud Storage Follow the next steps:
1. Create a bucket called "kubeconeu2021"
2. Create a service account that includes de Storage permissions to upload and download data from that bucket
3. Upload data/scores.csv into that bucket, this file will be used for the ETL container that generates and upload the model to the bucket

## Create Pipeline Containers
This section explains how to generate custom Docker images to test this small workflow. You can start moving to the containers folder with the next command:
```
cd containers
```
The containers included are:
- argo_deploy: Deploy your model using ArgoCD
- etl: Remove unnecesary fields from the csv and upload the generated file(scores_processed.csv) to your bucket
- model_training: Train a new model using the Linear Regression algorithm and upload the model(scores.model) to your bucket
- model_serve: Creates a basic API REST to get predictions from the model
- inference: Get Predictions from the exposed model
Note: For etl, model_serve and inference containers you need a service account json file called argok3s.json located inside each container folder in order to be pushed to DockerHub or your container registry of your choice.


### Create argo_deploy container
To generate the argo_deploy container follow the next steps:
1. Move to the argo_deploy folder
```
cd argo_deploy
```
2. Run the build command using your ArgoCD domain or subdomain, ArgoCD token and your DockerHub user
```
/bin/bash build.sh ARGOCD_DOMAIN ARGOCD_TOKEN DOCKERHUB_USER
```
3. Return to the containers folder
```
cd ..
```
Note: Use the ArgoCD token previously generated.

### Create ETL container
To generate your ETL container follow the next steps:
1. Move to the etl folder
```
cd etl
```
2. Run the build command using your DockerHub user
```
/bin/bash build.sh DOCKERHUB_USER
```
3. Return to the containers folder
```
cd ..
```

### Create Model Training container
To generate your Model Training container follow the next steps:
1. Move to the etl folder
```
cd model_training
```
2. Run the build command using your DockerHub user
```
/bin/bash build.sh DOCKERHUB_USER
```
3. Return to the containers folder
```
cd ..
```

### Create Model Serve container
To generate your Model Serve container follow the next steps:
1. Move to the etl folder
```
cd model_serve
```
2. Run the build command using your DockerHub user
```
/bin/bash build.sh DOCKERHUB_USER
```
3. Return to the containers folder
```
cd ..
```

### Create Inference container
To generate your Inference container follow the next steps:
1. Move to the etl folder
```
cd inference
```
2. Run the build command using your DockerHub user
```
/bin/bash build.sh DOCKERHUB_USER
```
3. Return to the containers folder
```
cd ..
```


### Running Argo Workflows Examples Manually
1. To execute an example from ArgoCD execute:
```
argo submit -n argo --serviceaccount argo --watch https://raw.githubusercontent.com/argoproj/argo/master/examples/hello-world.yaml
```
  
2. To run a simple pipeline that includes our hole experiment execute:
```
argo submit -n argo --serviceaccount argo --watch pipelines/mlops-simple-pipeline.yaml
```
To send parameters using argo submit you can use -p parameter, to customize your execution
```
argo submit -n argo --serviceaccount argo --watch pipelines/mlops-simple-pipeline.yaml -p annotation="Reason of Running the ML Pipeline"
```

3. To run a model deployment execute:
```
argo submit -n argo --serviceaccount argo --watch pipelines/mlops-model-deploy.yaml
```

## Configuring Argo Events for GitOps
To get some predictions from the model execute:
```
curl --header "Content-Type: application/json" \
--request POST --data '{"data":[17,17,25]}' \
http://mlops.tk/model1/predict
```

# Tested versions
- k3s, v1.20.4+k3s1
- helm, 3

## Troubleshooting
1. To explore the code of your container you can rewrite your entrypoint:
```
docker run -it --entrypoint /bin/sh czdev/argocd-deploy
```
2. To check all the enviroment variables execute in the terminal
```
printenv
```
3. To create a virtual environment execute:
```
virtualenv env1
source env1/bin/activate|deactivate
```

# References
Links used in this tutorial
- https://kinsta.com/blog/your-connection-is-not-private/
- https://virtualenv.pypa.io/en/latest/user_guide.html