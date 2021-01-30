docker run -it --env argoapp="model1" \
--env argotoken="token" \
--env replicaCount=3 \
--env containerPort=5431 \
--env dockerImage="czdev/model_serve" \
--env namespace="dev" \
--env appname="skmodel1" \
--env annotation="Final test :v" \
--env modelFilename="scores" \
--env bucket="BUCKET" \
czdev/argocd-cli

