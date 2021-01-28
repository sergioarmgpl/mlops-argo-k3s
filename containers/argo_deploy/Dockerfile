#RUN as: docker build --build-arg argodomain=URL -t argocd-cli .
FROM alpine:3.7
ARG argodomain
ENV argoserver=$argodomain
ENV argoapp="model"
ENV argotoken="token"
ENV replicaCount=3
ENV containerPort=5431
ENV dockerImage="xyz"
ENV namespace="dev"
ENV appname="model"
ENV annotation="new model"
ENV domain="model1.domain.tld"
ENV modelFilename="model1"
ENV bucket="bucket-sagemaker-test"
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
-p domain="$domain" \
-p modelFilename="$modelFilename" \
-p bucket="$bucket" \
-p aws_key="$aws_key" \
-p aws_secret="$aws_secret" \
-p aws_region="$aws_region" \
--auth-token $argotoken && \
argocd app --insecure --grpc-web \
--server $argoserver sync $argoapp \
--auth-token $argotoken
