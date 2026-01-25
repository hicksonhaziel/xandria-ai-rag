---
original_filename: devnet-validator-operators-1.txt
ingested_at: 2026-01-20
parts: 2
note: Large file - split into multiple sections
---

## Problem: Unable to Get Response from Commands
**@johnc:** 9/1/25, 10:01 AM
Running vNode and can't seem to get any response from commands "sb", "sg", or "sv". Validator is running and looks normal, but it does not seem to be communicating with the RPC.

* **@Substance 2.42:** RPC seems to be down, keep it running. Will report when everything is OK.
* **@Substance 2.42:** FYI, RPC is back online, so solana commands work.

## Problem: Delinquent Servers
**@csoaita:** 9/3/25, 9:09 AM
See 6 delinquent servers, is that too much?

* **@Substance 2.42:** There are 2 delinquent on current version, expect them to come back. 3 look like "abandoned" for a long time.

## Problem: Running mon.sh
**@david983:** 9/6/25, 6:47 PM
Anyone running mon.sh on their validator?

* **@Substance 2.42:** Running fine, including mon.sh. Your seems to be running OK too.
* **@david983:** Getting "thread 'main' panicked at validator/src/dashboard.rs:146.821" returning 'Result::unwrap()' on an 'ERR'.

## Problem: Upgrading to Herrenberg Version
**@NeoBubba:** 9/23/25, 6:18 PM
Call for upgrade to Herrenberg version. We are discontinuing pre-built binaries, please build from source.

* **@tupacalypse187:** Steps to build from source:
```bash
curl https://sh.rustup.rs -sSf | sh
source $HOME/.cargo/env
rustup component add rustfmt
rustup update
sudo apt update
sudo apt install libssl-dev libudev-dev pkg-config zlib1g-dev llvm clang cmake make libprotobuf-dev protobuf-compiler
git clone https://github.com/T3chie-404/agave-maint-util.git
cd agave-maint-util
chmod u+x start-upgrade.sh
./start-upgrade.sh x2.2.0-herrenberg
```
* **@csoaita:** Tried to upgrade but did not succeed.
* **@tupacalypse187:** Also try running this script:
```bash
https://github.com/T3chie-404/agave-maint-util/blob/main/system_tuning/system_tuner.sh
```

## Problem: Upgrading and Validator Version
**@mrhcon:** 9/24/25, 4:59 PM
Ran the upgrade script, but still see the old version.

* **@Substance 2.42:** Run system_tuner.sh before upgrading. Without this, you may still be running the previous version.
* **@Dean C:** Ran system_tuner.sh, post compiling fixed version issue, now on 7c3f39e8.
* **@csoaita:** Followed the steps and now everything seems OK.

## Problem: Upgrading with system_tuner.sh and start-upgrade.sh
**@Substance 2.42:** 9/26/25, 11:09 AM
Forget the "best of" guide and follow T3chie-404 GitHub readme for system_tuner.sh and then start-upgrade.sh.
```bash
cd ~
wget https://raw.githubusercontent.com/T3chie-404/agave-maint-util/refs/heads/main/system_tuning/system_tuner.sh
chmod a+x system_tuner.sh
./system_tuner.sh

wget https://raw.githubusercontent.com/T3chie-404/agave-maint-util/refs/heads/main/start-upgrade.sh
chmod a+x start-upgrade.sh
./start-upgrade.sh x2.2.0-herrenberg
```
* **@johnc:** Copy the above into the server that is running the vNode.
* **@apreston100:** Did the above, but validator is not running. Validator log could tell us more.

## Problem: Validator Not Running
**@apreston100:** 9/26/25, 9:18 PM
Did the upgrade, but validator is not running.
```bash
sudo systemctl start validator.service
sudo systemctl status validator.service
```
* **@Substance 2.42:** Validator is NOT running, can not say why. Validator log could tell us more.

---

## Problem: Upgrading and Setting Up
**@apreston100:** Just done all that and now seems to be upgraded and working. Thanks you **@Substance 2.42** and **@mrhcon**.

## Problem: Build and Compilation Issues
**@david983:** Im still not set up?:Build successful for x2.2.0-herrenberg.
Creating directory for compiled version: /home/sol/data/compiled/x2.2.0-herrenberg/bin
Syncing compiled binaries...
Build complete. Check artifacts in /home/sol/data/compiled/x2.2.0-herrenberg/bin. Press Enter to update active_release symlink...
Proceeding with symlink update...
ERROR: /home/sol/data/compiled/active_release exists but is not a symlink. Manual intervention required.
**@Substance 2.42:** There is some garbage on your disk, try this:
```bash
rm /home/sol/data/compiled/active_release
ln -s /home/sol/data/compiled/x2.2.0-herrenberg/bin /home/sol/data/compiled/active_release
systemctl restart validator.service
./catchup.sh
```
**@david983:** no solana commands seem to work ..tried above returned: "./catchup.sh: line 1: solana: command not found"...ill try as xand user see if that helps

## Problem: Solana Commands Not Working
**@NeoBubba:** Are you logged in as the SOL user and in the SOL directory?  "cd ~" before trying solana command.
**@david983:** Yes i was but the real issue was the recommended script effectively tried to "flip" active_release to the new herrenberg  build via dir not symlink. I created symlink to the release root not bin but could'nt run any solana commands because shell could'nt find agave-validator on my path i assume . I confirmed binaries as executable, bypassed PATH to run directly from bash. Then used "system-wide" symlink to keep PATH clean. Backup and running now ..,,,,.