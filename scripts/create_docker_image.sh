#! /bin/bash
cd ..
docker build -t davidsdeveloper/note-taker:v2 .
docker push davidsdeveloper/note-taker:v2