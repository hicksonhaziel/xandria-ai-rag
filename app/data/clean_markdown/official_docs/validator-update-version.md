---
original_filename: devnet.xandeum.network_validator-update-version_39c339aa.txt
source: https://devnet.xandeum.network/validator-update-version
ingested_at: 2026-01-20
---

## Introduction to Validator Update Version
To update your validator version, follow these steps:

## Update System Installation
Run the following commands as the `sol` user:
```bash
sudo apt-get update -y && sudo apt-get upgrade -y
```
Reboot if you need to load a newer kernel.

## Choose Which Release to Install
Go to the [Xandeum Binaries repo](https://github.com/Xandeum/binaries/releases/latest) and download the `tar.bz2` file to your server. Alternatively, set the version and filename variables:
```bash
ver="v2.2.0-xandeum_b5a94688"
file="v2.2.0-xandeum_b5a94688.tar.gz"
echo -e "\n"
echo version=$ver;
echo filename=$file
echo -e "\n"
```
Then, download the file using:
```bash
cd ~
wget https://github.com/Xandeum/binaries/releases/download/$ver/$file
```

## Create Needed Bin Folder and Extract File
Create the needed bin folder:
```bash
mkdir ~/.local/share/xandeum/install/releases/$ver -p
```
Extract the file into the new bin dir:
```bash
cd ~
tar -xf $file --directory ~/.local/share/xandeum/install/releases/$ver
```

## Add Directory for Connection Info and Test Binary
Add a directory for connection info:
```bash
sudo mkdir -p /var/run/xandeum && sudo chown sol:sol /var/run/xandeum && sudo chmod 755 /var/run/xandeum
sudo rm /var/run/xandeum/*
```
Test a binary by running it in the local folder:
```bash
cd ~/.local/share/xandeum/install/releases/$ver/bin
./agave-validator -V
```

## Remove Downloaded File and Set Symlink
Remove the downloaded file if binaries are working:
```bash
rm ~/$file
```
Set a symlink from the new release to the `active_release` folder:
```bash
rm /home/sol/.local/share/xandeum/install/releases/active_release
ln -sf /home/sol/.local/share/xandeum/install/releases/$ver/bin /home/sol/.local/share/xandeum/install/releases/active_release
```

## Check Install and Restart Validator
Check the install of the software from the home directory:
```bash
cd ~
agave-validator -V
```
Restart your validator:
```bash
agave-validator --ledger ~/ledger exit --max-delinquent-stake 10 --min-idle-time 0 --monitor
```