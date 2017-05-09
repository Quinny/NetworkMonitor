# NetworkMonitor

A home network monitor with a web UI.

# Setup

0. Clone the repo
1. Install the dependencies by running `./install_deps.sh` (Note Python 3.6+ is required for asyncio)
2. Fill in `settings.py` with your information
3. Configure the ping sweep cron job to update the state of the network.  See [cron/pingsweep.crontab](https://github.com/Quinny/NetworkMonitor/blob/master/cron/pingsweep.crontab) for an example which runs every 10 minutes
4. Start the Web UI `cd web && python3 main.py`.
5. (Optional) If you want to start the web UI as a service an [init.d script](https://github.com/Quinny/NetworkMonitor/blob/master/init.d/networkmonitor) has been provided, you just need to edit the `dir` and `user` variables
