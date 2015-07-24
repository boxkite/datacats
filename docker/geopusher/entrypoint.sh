#!/bin/bash

set -e

if [ ! -e /project ]; then
    echo "/project doesn't exist. Please mount it as a volume"
    exit 1
fi



exec "$@"
