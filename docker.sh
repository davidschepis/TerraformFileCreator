!/bin/bash
docker build -t toysrc .

docker network create db-network

docker run -d --network test-network --name test-mongo mongo:latest

docker run --network db-network --name mongodb -d -p 27017:27017 mongo

docker run --network db-network -it --name toycontainer -d -p 3456:80 toysrc

docker exec -it toycontainer bash

docker run -it --network db-network --rm mongo mongo --host mongodb test





#######
docker run --name db -d -p 27017:27017 mongo --noauth --bind_ip=0.0.0.0

docker run --name toycontainer -it -p 3013:80 -d --link db48c67a57da:27017 toysrc