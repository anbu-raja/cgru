#!/bin/bash

if [ -z $AF_ROOT ]; then
   pushd .. >> /dev/null
   source ./setup.sh
   popd >> /dev/null
fi
