#clear the old one
docker stop th
docker start th

#build it
docker build -t th .

#start up the new one
docker run -d \
  --name th \
  --restart unless-stopped \
  th:latest