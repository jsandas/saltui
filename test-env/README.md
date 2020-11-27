Testing

Start salt test env
```bash
./salt-env.sh start
```
Wait for admin password to be printed on screen
```bash
Pulling salt-master ... done
Pulling salt-minion ... done
salt-master is up-to-date
salt-minion is up-to-date

Switch to cli in salt-master container
```bash
./salt-env.sh cmd
```

Test module
```bash
salt \* userinfo.lastlog
```
