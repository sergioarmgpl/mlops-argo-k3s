docker run -it --env argoapp="skmodel1" \
--env argotoken="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MDQ4NjE4OTgsImlzcyI6ImFyZ29jZCIsIm5iZiI6MTYwNDg2MTg5OCwic3ViIjoiYWRtaW4ifQ.h9Mhzw8l0kKuSrvdSCp_uUZ1a_izdKuF5s0SgxMIN6Y" \
--env replicaCount=3 \
--env containerPort=5431 \
--env dockerImage="570959708571.dkr.ecr.us-east-1.amazonaws.com/sklearn_models" \
--env namespace="dev" \
--env appname="skmodel1" \
--env annotation="Final test :v" \
--env domain="model1.wzpocs.tk" \
--env modelFilename="scores" \
--env bucket="sergio-sagemaker-test" \
czdev/argocd-cli

