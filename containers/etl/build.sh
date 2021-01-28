docker login
#docker build --no-cache -t czdev/scoresml .
docker build -t $1/scoresml .
docker push $1/scoresml
