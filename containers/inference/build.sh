#run as ./build DOCKERHUB_USER
docker login -u $1
docker build -t $1/inference .
docker push $1/inference
