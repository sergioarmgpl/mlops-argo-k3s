#RUN as: docker build --build-arg argodomain=URL argotoken=TOKEN -t argocd-deploy .
FROM alpine:3.7
ARG argodomain
ARG argotoken
ENV argoserver=$argodomain
ENV argoapp="model"
#ENV argotoken="token"
ENV argotoken=$argotoken
ENV replicaCount=3
ENV containerPort=5431
ENV dockerImage="xyz"
ENV namespace="dev"
ENV appname="model"
ENV annotation="new deploy"
ENV modelFilename="model1"
ENV bucket="bucket"
RUN apk add curl
RUN curl -sSL -k -o argocd https://$argodomain/download/argocd-linux-amd64
RUN chmod 755 argocd
RUN mv argocd /bin
ENTRYPOINT argocd app --insecure --grpc-web --server $argoserver \
set $argoapp \
-p replicaCount=$replicaCount \
-p containerPort=$containerPort \
-p dockerImage="$dockerImage" \
-p namespace="$namespace" \
-p appname="$appname" \
-p annotation="$annotation" \
-p modelFilename="$modelFilename" \
-p bucket="$bucket" \
--auth-token $argotoken && \
argocd app --insecure --grpc-web \
--server $argoserver sync $argoapp \
--auth-token $argotoken
