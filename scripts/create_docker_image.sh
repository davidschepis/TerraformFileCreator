#! /bin/bash
echo "Version Number is now $1"
echo "Building new image"
docker build -t davidsdeveloper/note-taker:v$1 .
sleep 1
echo "Pushing new image to docker hub"
docker push davidsdeveloper/note-taker:v$1
sleep 1