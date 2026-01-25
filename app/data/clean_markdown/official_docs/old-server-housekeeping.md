---
original_filename: devnet.xandeum.network_old-server-housekeeping_79be27dd.txt
source: https://devnet.xandeum.network/old-server-housekeeping
ingested_at: 2026-01-20
---

## Old Server Housekeeping
Run as sudo / root user
Reboot if you have a new kernel installed during the update that needs loaded.
```bash
sudo -s &&
apt-get update -y && apt upgrade
```
## Stop Old System Service
Use `status` to check if it's running, `stop` to stop the service, and `disable` to prevent it from loading next reboot
```bash
systemctl status xand.service
systemctl disable xand.service
systemctl stop xand.service
```
## SSH Keys
If you want to make a new user `sol` to match the new guide, then make sure your ssh keys to login remotely are stored in your home dir for `sol` or `root` users (not only in `xand` home dir. Careful with the ssh keys...if you remove them you could lock yourself out of your server...
Check for keys in root
```bash
sudo cat ~/.ssh/authorized_keys
```
Check for keys in `xand`
```bash
su xand
cd ~
cat ~/.ssh/authorized_keys
```
Copy from `xand` and append to root keys file
```bash
sudo -i
sudo cat /home/xand/.ssh/authorized_keys >> /root/.ssh/authorized_keys
```
## Validator Keypairs
Make sure you have copied your validator keypairs if they are needed for the new server.
Otherwise, they can be created new during install of the validator software.
There is no reason to re-use the old one, only personal preference.
## Remove Xand User Account
Once you have successfully logged into your server using either `root` or `sol` user, and copied/backed up any files you need, you may wish to remove everything from `xand` user and their files.
```bash
sudo -s
userdel -rf xand
```