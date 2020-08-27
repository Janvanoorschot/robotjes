#!/usr/bin/env bash
# Builds the robotjes (development) environment.

# get the root directory
CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DIR="$(dirname "$CURDIR")"
export DOCKERDIR=$DIR/docker

# spec the current version
VERSION=1.0

# spec some of the special dirs
export RM_ROBOTJES=/data/dev/robotjes

# create the docker images
cd $DOCKERDIR
docker build -f $DOCKERDIR/Dockerfile-postgres -t robomind/postgres:$VERSION .
cd $DOCKERDIR
docker build -f $DOCKERDIR/Dockerfile-rabbitmq -t robomind/rabbitmq:$VERSION .
cd $DIR
docker build -f $DIR/Dockerfile -t robomind/robotjes:$VERSION .
