#!/bin/bash

docker rm -f hacker-box
docker build --tag hacker-box docker
docker run -d -p 4040-4080:4040-4080 --name hacker-box -v $(pwd):/home/hacker/CTF-tools:rw hacker-box
