---
original_filename: devnet.xandeum.network_validator-installation_4a951223.txt
source: https://devnet.xandeum.network/validator-installation
ingested_at: 2026-01-20
---

## Introduction to Validator Installation
To setup a Xandeum DevNet validator, follow these steps:

## 1) Update and Setup User
Start with a fresh instance of Linux as the root user. These instructions use Ubuntu Server 22.04.2LTS.

* Run as sudo or root user.
* Update your installation:
  ```bash
sudo apt-get update -y
sudo apt-get upgrade -y
```
* Install a few apps:
  ```bash
sudo apt install -y bzip2 vnstat
sudo systemctl enable --now vnstat
```

## 2) Choose Release to Install
Go to the Xandeum Binaries repo and download the tar.bz2 file to your server.
* Set the version and filename variables:
  ```bash
ver="v2.2.0-xandeum_b5f66263"
file="v2.2.0-xandeum_b5f66263.tar.gz"
```
* Download the file:
  ```bash
cd ~
wget https://github.com/Xandeum/binaries/releases/download/$ver/$file
```
* Create the needed bin folder:
  ```bash
mkdir ~/.local/share/xandeum/install/releases/$ver -p
```
* Extract the file into the new bin dir:
  ```bash
sudo mkdir -p /var/run/xandeum && chown sol:sol /var/run/xandeum && chmod 755 /var/run/xandeum
```
* Test a binary by running it in the local folder:
  ```bash
cd ~/.local/share/xandeum/install/releases/$ver/bin
./agave-validator -V
```

## 3) Configure Validator Instance
Please observe proper security of your private keys.
* Generate your 3 DevNet keys:
  ```bash
solana-keygen new -o ~/validator-keypair.json
solana-keygen new -o ~/vote-keypair.json
solana-keygen new -o ~/withdraw-keypair.json
```
* Switch to Xandeum cluster:
  ```bash
solana config set --url https://api.devnet.xandeum.com:8899
```
* Set your new keypair to be used by default:
  ```bash
solana config set --keypair ~/validator-keypair.json
```
* Testing our work so far:
  ```bash
solana gossip
solana airdrop 1 ~/validator-keypair.json
```
* Create your vote account:
  ```bash
solana create-vote-account --commission 0 ~/vote-keypair.json ~/validator-keypair.json ~/withdraw-keypair.json
```

## 4) Configure Start Script Configuration
Create your validator configuration file using your editor:
```bash
vim ~/validator-start.sh
```
Add the following configurations:
```bash
#!/bin/bash
exec agave-validator \
        --known-validator G6x4w89TJA9oDBSRNcpeanaThqBUJbEv5DJRBZGrQHYV \
        --known-validator 5PW1SsXftQqKLF9FU88898BMG1vv3tqYRrVkGkFRwobs \
        --known-validator 96wn2RrHFxXNMNJCN64qZCpBPCkHVTuKfWoeRTGrCdDy \
        --known-validator DiEyTNni4uPwXaj9AX4pvFWvYFY5FKLEo3RRgN6Q22Lc \
        --known-validator 9HKXdh8Veb278efwgPjsRkQtyJEGhyGP8vkbCSmp4HgR \
        --entrypoint xand-5.devnet.xandeum.com:8000 \
        --entrypoint xand-4.devnet.xandeum.com:8000 \
        --entrypoint xand-3.devnet.xandeum.com:8000 \
        --entrypoint xand-2.devnet.xandeum.com:8000 \
        --entrypoint xand-1.devnet.xandeum.com:8000 \
        --expected-shred-version 48698 \
        --expected-genesis-hash 7BNTf1Z8KDUb3yCsNiVS5XH1CxfYG3HQP2VeHMVqP7AW \
        --snapshot-interval-slots 500 \
        --full-snapshot-interval-slots 10000 \
        --identity ~/validator-keypair.json \
        --vote-account ~/vote-keypair.json \
        --ledger ~/ledger/ \
        --dynamic-port-range 8000-10000 \
        --rpc-port 8899 \
        --log ~/validator.log \
        --no-poh-speed-test \
        --limit-ledger-size 30000000
```
Make the script executable:
```bash
chmod a+x ~/validator-start.sh
```

## 5) System Tuning
Run as root user, use `sudo -i`.
* Optimize sysctl knobs:
  ```bash
sudo bash -c "cat >/etc/sysctl.d/21-agave-validator.conf <<EOF
net.core.rmem_default = 134217728
net.core.rmem_max = 134217728
net.core.wmem_default = 134217728
net.core.wmem_max = 134217728
vm.max_map_count = 2000000
fs.nr_open = 2000000
EOF"
```
* Apply the changes:
  ```bash
sudo sysctl -p /etc/sysctl.d/21-agave-validator.conf
```
* Open the file `/etc/systemd/system.conf` in your editor and add the following to the `[Manager]` section:
  ```bash
DefaultLimitNOFILE=2000000
```
* Reload the daemon:
  ```bash
sudo systemctl daemon-reload
```
* Increase process file descriptor count limit:
  ```bash
sudo bash -c "cat >/etc/security/limits.d/90-agave-nofiles.conf <<EOF
* - nofile 2000000
EOF"
```