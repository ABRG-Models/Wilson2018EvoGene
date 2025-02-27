PWD=`pwd | awk -F'/' '{ print $NF }'`
if [ ${PWD} = 'supp' ]; then
    pushd ../..
else
    echo "Please run this from the scripts/supp directory."
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
