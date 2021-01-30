# MLOPS USING ARGO & K3S

## K3s installation
sudo apt-get update

PUBLIC_IP=YOUR_IP
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --tls-san "$PUBLIC_IP" --node-external-ip "$PUBLIC_IP" --write-kubeconfig-mode 644" sh -s -

kubectl get nodes

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh



ssh -i id_rsa developer@argok3s.tk cat /etc/rancher/k3s/k3s.yaml > ~/.kube/con
fig

Modify
server: https://argok3s.tk:6443

## Nginx ingress controller Installation
Local machine
kubectl create ns ingress-nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx 
helm repo update 
helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx


## Argo Workflows Installation

kubectl create ns argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml



kubectl patch configmap/workflow-controller-configmap \
-n argo \
--type merge \
-p '{"data":{"containerRuntimeExecutor":"k8sapi"}}'

kubectl get pods -n argo

kubectl -n argo port-forward deployment/argo-server 2746:2746


argo submit -n argo --serviceaccount argo --watch https://raw.githubusercontent.com/argoproj/argo/master/examples/hello-world.yaml

argo submit -n argo --serviceaccount argo --watch pipelines/mlops.yaml


## ArgoCD Installation
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


kubectl apply -f argocd/argocd-ingress.yaml

### ArgoCD Password
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2

curl -sSL -k $ARGOCD_SERVER/api/v1/session -d $'{"username":"admin","password":"argocd-server-5d7d9b7f9c-x8l7n"}'

