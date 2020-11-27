#!/bin/bash	

START=0	
STOP=0	
RELOAD_MINION=0	
SALTCMD=0	
SALTUICMD=0

COMPOSE_COMMAND="docker-compose -f docker-compose_dev.yml"

salt_docker_shell () {	
    docker exec -it -w /srv salt-master sh	
}	

saltui_docker_shell () {	
    docker exec -it -w /opt/saltui saltui sh	
}	

start () {	
    $COMPOSE_COMMAND pull	
    $COMPOSE_COMMAND up -d	

    # sync salt files for the first time	
    sleep 10
    docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1
}	

stop () {	
    $COMPOSE_COMMAND down	
}	

usage () {	
    echo "invalid input"	
    echo " Usage:" 	
    echo " ./salt-env (start|stop|cmd|saltcmd)"	
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
        saltcmd)	
        SALTCMD=1	
        shift # past argument	
        ;;
        cmd)	
        SALTUICMD=1	
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
elif [[ $SALTCMD -gt 0 ]]; then	
    salt_docker_shell
elif [[ $SALTUICMD -gt 0 ]]; then	
    saltui_docker_shell	
else	
    usage	
fi 