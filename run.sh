#!/bin/bash

docker run --privileged --name $2 -v $3:/root/nslab/rawTraffic -d $1
