---
original_filename: devnet-anouceM.txt
source: https://devnet.xandeum.network/validator-update-version
ingested_at: 2026-01-20
---

## Problem: Upgrading vNodes to v2.2.0-xandeum_b5a94688
**@DevNet:** Please upgrade your vNodes as soon as possible to the v2.2.0-xandeum_b5a94688 release. For most users, use the pre-built binaries and the standard guide: https://devnet.xandeum.network/validator-update-version. To build from source, use the branch: https://github.com/Xandeum/xandeum-agave/tree/x2.2.0-munich.

## Problem: Checking vNode Version
**@DevNet:** To check the build version, use the command: `agave-validator -V`. The current version should be: `agave-validator 2.2.0 (src:b5a94688; feat:3294202862, client:Xandeum)`.

## Problem: Upgrading pNodes to Munich
**@DevNet:** It's time to upgrade your pNodes to Munich. Use the guide: https://pnodes.xandeum.network/pnode-update-version.

## Problem: Update to install.sh Script
**@DevNet:** There was an update pushed to the install.sh script. The update will help handle reboots and instances where pod.service is failed and will not start. Run the new install.sh with Option 3 - Restart to enable a config file at reboot.

## Problem: Upgrading to Herrenberg Version
**@DevNet:** Upgrade to the Herrenberg version: https://github.com/Xandeum/xandeum-agave/tree/x2.2.0-herrenberg. Build from source, as pre-built binaries are discontinued. A system tuning script is available to setup a new server or migrate an existing one: https://github.com/T3chie-404/agave-maint-util.

## Problem: pNode Onboarding
**@DevNet:** pNode onboarding is open. Go to https://pnode-onboarding.paperform.co/ and fill out the form. If you have trouble, check your connection, try another browser, or open a ticket on https://help.xandeum.network/.

## Problem: pNode Payout Announcements
**@DevNet:** July, August, and September pNode payouts are available. Proposals are available at:
- https://dao.xandeum.network/dao/XAND/proposal/8mSLZWPzPtsn63AiMuUs1kMHUP4pzxGrqtqGSCJFwPg6
- https://dao.xandeum.network/dao/XAND/proposal/2AJgQ8Tc83r1eRcHxNnbWKZirweWxrogGnfQhdMhar4G
- https://dao.xandeum.network/dao/XAND/proposal/9dsQH11fKKVHBixw5MWuWgaV27iB6cJXEbQc4HeDiNf1
- https://dao.xandeum.network/dao/XAND/proposal/6r2CKH8tekAauLTD7eucE2pgtBJTHvjVg6tXz2FzGihZ
- https://dao.xandeum.network/dao/XAND/proposal/5w16mZMqGy6HA1Y3vkKydN7H2g64SjCqD1pxi7EMqCTU
- https://dao.xandeum.network/dao/XAND/proposal/34acZLbBSw2KDSj6JDkM2k9qTYGo9z7kg124o6zByE4A

## Problem: vNode Payout Announcements
**@DevNet:** August and September vNode payouts are available. Proposals are available at:
- https://dao.xandeum.network/dao/XAND/proposal/DiAAtx8nc9asg8mHCq8tLwCkJQMsvHyZMFtnnCsHEe7x
- https://dao.xandeum.network/dao/XAND/proposal/6u1K6iv2nGYcgXKnbNPfN2jmbL5PJRuK73VkuSU8j53x

## Problem: Backing up Operator Keypairs
**@DevNet:** Make sure to back up your operator keypairs to a safe location. For pNode operators, the key is located at: `/root/xandminerd/keypairs/pnode-keypair.json`. For vNode operators, the keys are located at:
- `/home/sol/validator-keypair.json`
- `/home/sol/vote-keypair.json`
- `/home/sol/withdraw-keypair.json`

## Problem: Fixing Key Pair Permissions
**@DevNet:** Fix key pair permissions using the following commands:
```bash
sudo chmod 600 /local/keypairs/pnode-keypair.json
sudo chown root:root /local/keypairs/pnode-keypair.json
```
Verify the permissions using:
```bash
ls -la /local/keypairs/pnode-keypair.json
```
Expected output:
```bash
-rw------- 1 root root
```
Test that a local basic user can't read the file using:
```bash
sudo -u <non-sudo-username> cat /local/keypairs/pnode-keypair.json
```
Expected output:
```
cat: pnode-keypair.json: Permission denied
```

## Problem: Running a pNode without a License
**@DevNet:** To run a pNode without a license, use the following commands as root user:
```bash
fallocate /xandeum-pages -l 10g
ln -s /xandeum-pages /run/xandeum-pod
```
Adjust the size to what you want to allocate and then check the service using:
```bash
sudo systemctl status pod.service
```

## Problem: Upgrading to v0.7.0
**@DevNet:** Upgrade your pNode servers to v0.7.0 using the following command:
```bash
sudo wget -O install.sh "https://raw.githubusercontent.com/Xandeum/xandminer-installer/refs/heads/master/install.sh" && sudo chmod a+x install.sh && sudo ./install.sh
```

## Problem: Upgrading to v0.7.3
**@DevNet:** Upgrade your pNode servers to v0.7.3 using the following commands:
```bash
cd ~ && wget -O install.sh "https://raw.githubusercontent.com/Xandeum/xandminer-installer/refs/heads/master/install.sh" && chmod a+x install.sh && ./install.sh
```
Use Option 2 to upgrade.

## Problem: Upgrading to v0.8.0
**@DevNet:** Upgrade your pNode servers to v0.8.0 using the following commands:
```bash
cd ~ && wget -O install.sh "https://raw.githubusercontent.com/Xandeum/xandminer-installer/refs/heads/master/install.sh" && chmod a+x install.sh && ./install.sh
```
Use Option 2 to upgrade. Check the running version after install using:
```bash
curl -s -X POST http://localhost:6000/rpc \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"get-version","id":1}' | \
jq -r '.result.version as $v | "xandminer: \($v) xandminerd: \($v) pod: \($v)"'
```
Expected output:
```
xandminer: 0.8.0 xandminerd: 0.8.0 pod: 0.8.0
```

## Problem: pNode Credits
**@DevNet:** pNode credits are available at:
- https://podcredits.xandeum.network/ (mainnet)
- https://podcredits.xandeum.network/devnet (devnet)
API endpoints:
- https://podcredits.xandeum.network/api/pods-credits (devnet)
- https://podcredits.xandeum.network/api/mainnet-pod-credits (mainnet)

## Problem: Updating @MainNet and @RPC Operator Roles
**@DevNet:** Add roles for @MainNet and @RPC Operator where applicable. Update to version 3.0.14 ASAP for an exploit that was detected. The new branch is available at: https://github.com/Xandeum/xandeum-agave/tree/v3.0.14-upgrade.