---
original_filename: devnet.xandeum.network_troubleshooting_e139b03d.txt
source: https://devnet.xandeum.network/troubleshooting
ingested_at: 2026-01-20
---

## Troubleshooting
Some things to try when experiencing issues with your validator.

## Balance
Run the `catchup.sh` script first. If you're caught up but your validator is delinquent, then check your `validator-keypair.json` balance.
```bash
solana balance validator-keypair.json
```
Check the Identity Account balance, as you need to pay fees out of this account to vote on transactions.

## Stake
If you're online but not in the xandeum validators list, check if there are any tokens staked to your vote account. If not, follow up with Labs to get you staked.
```bash
solana stakes ~/vote-keypair.json
```
If it shows a stake account, but has the phrase "Stake account is undelegated", then it means you were delinquent at some point and your stake was removed to lower the delinquency level.

## Connections
Restart your validator and watch for the TCP connections to succeed:
```bash
sudo systemctl restart validator.service &&
tail -f ~/validator.log | grep --color=always -B 10 -A 50 "Checking that tcp ports"
```
Look for the ports to be "reachable":
* tcp/8899
* tcp/8900
* tcp/8000
This will tell you a lot about your router environment. If it fails the first time, it will try again. UDP is important too, but usually the first indicator of trouble is TCP.