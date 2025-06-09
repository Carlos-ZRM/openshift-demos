#!/bin/bash

name=app-base
oc new-build --name $name --binary --strategy docker

oc start-build  $name  --from-dir .  --follow
