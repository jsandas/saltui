#!/bin/bash

START=0
STOP=0
RELOAD_MINION=0
CMD=0

docker_shell () {
    docker exec -it -w /usr/src/app salt-master ash
}
    
start () {
    docker-compose pull
    docker-compose up -d

    # dependencies required for gitfs testing
    # echo ""
    # echo "installing dependencies..."
    # docker exec salt-master sh -c "apk --no-cache add git libgit2-dev && pip3 install pygit2"

    # sync salt files for the first time
    docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1
    docker-compose restart salt-minion

}

stop () {
    docker-compose down
}

reload () {
    docker exec -it salt-master salt-key -D -y
    docker rm -f salt-minion
    docker-compose up -d    
}

usage () {
    echo "invalid input"
    echo " Usage:" 
    echo " ./salt-env (start|stop|reload|cmd) ARGS"
    echo ""
}

while [[ $# -gt 0 ]]
do
    key=$1
    case "$key" in
        start)
        START=1
        shift # past argument
        ;;
        stop)
        STOP=1
        shift # past argument
        ;;
        reload)
        RELOAD_MINION=1
        shift # past argument
        ;;
        cmd)
        CMD=1
        shift # past argument
        ;;
    esac
done

if [[ $START -gt 0 ]]; then
    start
elif [[ $STOP -gt 0 ]]; then
    stop
elif [[ $RELOAD_MINION -gt 0 ]]; then
    reload
elif [[ $CMD -gt 0 ]]; then
    docker_shell
else
    usage
fi