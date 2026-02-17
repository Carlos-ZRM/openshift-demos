#!/bin/bash

name=app-base

podman build -t $name  .
podman run --rm -it --name $name -p 5000:5000 $name