#!/usr/bin/env bash
SCRIPTNAME=$0

usage()
{
echo "Usage: $SCRIPTNAME {name:tag}"
}

[ "$#" != "1"  ] && usage && exit 0

IMAGE_NAME=$1

build_args=""
if [ ! -z $https_proxy ]
then
    build_args="$build_args --build-arg https_proxy=$https_proxy"
fi

if [ ! -z $http_proxy ]
then
    build_args="$build_args --build-arg http_proxy=$http_proxy"
fi

if [ ! -z $no_proxy ]
then
    build_args="$build_args --build-arg no_proxy=$no_proxy"
fi

echo "docker build $build_args --no-cache -t ${IMAGE_NAME} ."
docker build $build_args --no-cache -t ${IMAGE_NAME} .
