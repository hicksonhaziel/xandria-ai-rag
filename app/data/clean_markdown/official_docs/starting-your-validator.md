---
original_filename: devnet.xandeum.network_starting-your-validator_0485aa38.txt
source: https://devnet.xandeum.network/starting-your-validator
ingested_at: 2026-01-20
---

## Starting Your Validator
There are two methods to start your validator. Only run one method or the other. If you have followed the guide, then proceed to option 2 below to start as a background service.

### Manual Method
Manual will require you to keep the terminal window open or use a terminal multiplexor (tmux) as the validator will die if the window closes.
```bash
cd ~
./validator-start.sh
```

### System Service (Auto) Method
The service will run in the background and will auto start 1 second after the system reboots. 
> NOTE: complete the section Setup System Service first.

Run as sudo or root user:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now validator.service
```
Check if the service started and stayed running:
```bash
sudo systemctl status validator.service
```
> Note: You should see the service is active (running) and you should see no exit code in the log at the bottom of the status window as shown below. Press q to quit.