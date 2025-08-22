# Scheduler
- Author Kyle
- Version 20250822v1
- Email <kyle@hacking-linux.com>
- A new crontab suppose to trigger jobs as per sec.

## Quick Start
### Deploy Guide
- Install Miniforge
Pls refer to below repo.
https://github.com/kylechenoO/miniforge

- Enable project env

```
$ source bin/activate
```

- Install dependences

```
$ tools/install_offline_pkg.sh
$ deactivate
```

- Config jobs

```
$ vim etc/jobs.conf
## Sample:
## *   *   *   *     *       cmd
## sec min day month weekday command
## * * * * * * echo ">> $(date +%Y%m%d%H%M%S) Hello per 1 seconds"
## */5 * * * * * echo ">> $(date +%Y%m%d%H%M%S) Hello per 5 seconds"
## PLEASE ADD YOUR JOBS UNDER THIS
```

- Start service on console

```
$ sudo /opt/miniforge/bin/python bin/Scheduler.py
```

- Add to systemd
Please ensure the path of the project is correct.

```
$ sudo cp -rvf systemd/scheduler.service /etc/systemd/system/scheduler.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable scheduler
$ sudo systemctl restart scheduler
$ sudo systemctl status scheduler
```

## Debug Procedures
- logs under log/

```
$ tail -f log/scheduler.log
```
