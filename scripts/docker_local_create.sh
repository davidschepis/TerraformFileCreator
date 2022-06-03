#!/bin/bash
echo "Running local contaienr note-taker:v$1"
docker run -it --name notetaker -d -p 3001:3001 davidsdeveloper/note-taker:v$1