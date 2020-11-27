# SaltUI

This is a basic project which displays information retrieved from salt

If using salt-api, this can be run anywhere that has access to the salt-api endpoints 
with or without docker.
Otherwise it must be run locally on the salt master without docker.


##Run app:

Docker:
```bash
docker-compose up -d
```

Without docker (recommend using python virtualenv):

Setup virtualenv (optional):
```bash
yum install python-virtualenv
virtualenv -p 3 .venv
```

Start application:
```bash
source .venv/bin/activate
./start.sh
```

##Collecting data from:
Data is collected running the following commands.  These can be ran manually or using a scheduler such as cron or jenkins. 
Note:: retrieving users information requires the `userinfo.py` module in the salt_modules folder to be added to the _modules folder of the salt file root (/srv/salt/_modules)

```bash
./update.sh system
./update.sh package
./update.sh users
```
Or:
```bash
./update.sh all
```

# Dev
Use the docker-compose_dev.yml docker compose file to bring up the dev environment.  Currently migrations
have to be run manually update the contaiers are up.

```bash
docker-compose -f docker-compose_dev.yml exec saltui python manage.py migrate
```
To populate data from test salt-minion
```bash
docker-compose -f docker-compose_dev.yml exec saltui sh -c "update.sh all"
```