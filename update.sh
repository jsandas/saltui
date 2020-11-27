#!/bin/sh

SALTUI_PATH=$PWD
PYTHON=$(which python)

system () {
    echo "Updating systems information..."
    $PYTHON $SALTUI_PATH/manage.py systeminfo --target '*'
}

packages () {
    echo "Updating packages information..."
    $PYTHON $SALTUI_PATH/manage.py packages --target '*'
}

users () {
    echo "Updating users information..."
    $PYTHON $SALTUI_PATH/manage.py users --target '*'
}

all () {
    system
    packages
    users
}

usage () {
    echo ""
    echo "Usage: update.sh system|packages|users|all"
}

# MAIN FUNCTION
case "$1" in
    system)
        system
        shift # past argument 
        ;;
    packages)
        packages
        shift # past argument
        ;;
    users)
        users
        shift # past argument
        ;;
    all)
        all
        shift # past argument
        ;;
    *)
        usage
        shift # past argument
        ;;
esac
