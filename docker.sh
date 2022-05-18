!/bin/bash
docker build -t notes .

docker run -it --name notetaker -d -p 3001:3001 notes