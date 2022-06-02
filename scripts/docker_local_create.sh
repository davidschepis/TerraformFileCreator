#!/bin/bash
docker run -it --name notetaker -d -p 3001:3001 davidsdeveloper/note-taker:$1