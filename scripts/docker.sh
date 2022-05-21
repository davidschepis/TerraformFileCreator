!/bin/bash
cd ..
docker build -t note-taker .
docker run -it --name notetaker -d -p 3001:3001 notes