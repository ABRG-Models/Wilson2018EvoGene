#!/bin/bash

PWD=`pwd | awk -F'/' '{ print $NF }'`
if [ ${PWD} = 'scripts' ]; then
    pushd ..
elif [ ${PWD} = 'simsj' ]; then # This line will change
    pushd .
else
    echo "Please run this from simsj or the scripts directory."
fi

# Find out where to run from.
HN=`hostname`
if [ ! -d ${HN} ]; then
    if [ -d build ]; then
        echo "No directory '${HN}'; defaulting to the directory 'build'"
        HN=build
    else
        echo "Please build the software using cmake in a directory called '${HN}' or 'build'."
        exit 1
    fi
fi

echo "Using build directory ${HN} for executables"

# Run several evolves in parallel.
./${HN}/sim/prob_fitinc 0.02 &
./${HN}/sim/prob_fitinc 0.05 &
./${HN}/sim/prob_fitinc 0.1 &
./${HN}/sim/prob_fitinc 0.2 &
./${HN}/sim/prob_fitinc 0.3 &
./${HN}/sim/prob_fitinc 0.4 &
./${HN}/sim/prob_fitinc 0.5 &

wait
popd
