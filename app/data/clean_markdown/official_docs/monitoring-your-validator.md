---
original_filename: devnet.xandeum.network_monitoring-your-validator_afebd477.txt
source: https://devnet.xandeum.network/monitoring-your-validator
ingested_at: 2026-01-20
---

## Monitoring your validator
To monitor your validator, you can tail your log file to watch the latest entries for errors. 

### Tail your log file
Run the following commands as the `sol` user:
```bash
su sol
cd ~
tail -f ~/validator.log
```
You can also grep the log file for specific search terms:
```bash
tail -f ~/validator.log | grep "search terms"
```
To restart your validator and grep the log file for initial connection info:
```bash
sudo systemctl restart validator.service &&
tail -f ~/validator.log | grep --color=always -B 10 -A 50 "Checking that tcp ports"
```

## mon.sh
Create a monitor script to easily run the monitor command.

### Create mon.sh
Run the following commands as the `sol` user:
```bash
cd ~
vim mon.sh
```
Copy the following code into the file, correcting your ledger path if needed:
```bash
agave-validator --ledger ~/ledger monitor
```
Make the file executable:
```bash
chmod a+x mon.sh
```
Run the monitor from your home directory:
```bash
cd ~
./mon.sh
```
Note: Press enter to drop a line to compare old values and press ctrl+c to exit the monitor command.

## catchup.sh
Create a catchup script that compares your machine to the RPC that you are connected to.

### Create catchup.sh
Run the following commands as the `sol` user:
```bash
cd ~
vim catchup.sh
```
Copy the following code into the file:
```bash
solana catchup -k ~/validator-keypair.json --our-localhost --follow --verbose
```
If using the ALT method for catchup, use the following code instead:
```bash
solana catchup -k ~/validator-keypair.json --our-localhost --follow --verbose
```
Make the file executable:
```bash
chmod a+x catchup.sh
```
Run the catchup script from your home directory:
```bash
cd ~
./catchup.sh
```
Note: Press enter to drop a line to compare old values and press ctrl+c to exit the catchup command.

## Watchtower
Watchtower is an optional monitoring system that runs on a separate computer and alerts you in your own personal Discord.

### Setup Watchtower
Watchtower should be run from a remote computer that is running 24/7. You will need to create a Discord or Slack channel with a webhook to make this work.

### Example Script
Create a script named `watchtower-alerts.sh` with the following content:
```bash
export DISCORD_WEBHOOK=https://discord.com/api/webhooks/xxxxxxx/yyyyyyyyyy
export SLACK_WEBHOOK=https://hooks.slack.com/services/xxxxxxxxx/yyyyyyyy/zzzzzz

#! /bin/sh
exec agave-watchtower \
         --url https://api.devnet.xandeum.com:8899/ \
         --validator-identity <Validator ID> \
         --name-suffix ::<Alert>:: \
         --interval 300 \
         --unhealthy-threshold 3 \
         --minimum-validator-identity-balance 3
```
Make the file executable:
```bash
chmod a+x watchtower-alerts.sh
```
Run the script:
```bash
./watchtower-alerts.sh
```
Note: You may want to run this script in a tmux session so it stays active when you close your terminal.