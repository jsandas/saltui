# SaltUI

This is a basic project which displays information retrieved from salt

If using salt-api, this can be run anywhere that has access to the salt-api endpoints 
with or without docker.
Otherwise it must be run locally on the salt master without docker.


**Run app:**

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

**Default superuser login credentials:**
user: admin
password: password

Note:: default superuser can be changed with env vars:
```
DJANGO_SUPERUSER_EMAIL=name@test.com
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=secretpassword
```

##Dev
Use make to run dev environment

Build dev environment:
```bash
make build-dev
```

Start dev environment:
```bash
make run-dev
```

Use cli in saltui container:
```bash
make saltui-cmd
```

Stop dev environment:
```bash
make stop-dev
```

Create clean dev environment:
```bash
make fresh
```

##Saltui commands:
**Collecting data from:**
Data is collected running the following commands.  These can be ran manually or using a scheduler such as cron, jenkins, or ophelia. 
Note:: retrieving users information requires the `userinfo.py` module from the /srv/salt/_modules folder to be added to the salt file root (/srv/salt/_modules)

```bash
./update.sh system
./update.sh package
./update.sh users
```
Or:
```bash
./update.sh all
```