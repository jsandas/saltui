#!/bin/sh
set -e

# Get the postgres user or set it to a default value
pg_user="postgres"
if [ ! -z $POSTGRES_USER ]; then 
    pg_user=$POSTGRES_USER
fi

# Get the postgres db or set it to a default value
pg_db=$pg_user
if [ -n $POSTGRES_DB ]; then 
    pg_db=$POSTGRES_DB
fi

if [ ! -z "$POSTGRES_APP_USER" ]; then
echo $pg_user
echo $pg_db
psql -v ON_ERROR_STOP=1 -U "$pg_user" -d "$pg_db" <<-EOSQL
    CREATE USER $POSTGRES_APP_USER NOSUPERUSER PASSWORD '$POSTGRES_APP_PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE $pg_db TO $POSTGRES_APP_USER;
EOSQL
fi


