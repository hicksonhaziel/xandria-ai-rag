---
original_filename: support1.txt
ingested_at: 2026-01-20
---

## Problem: Port Binding Error
**@Ymetro:** 5/28/25, 10:11 AM
I am getting a `bind [127.0.0.1]:3000/4000: Permission denied` error when trying to connect to my VPS/PC. I changed nothing in the command line to SSH into the VPS/PC, but it does not connect anymore.

## Solution
* Check if the port is already in use by going to `http://localhost:3000/` in your browser.
* Ensure you are running the SSH command on the correct machine (not the pNode).
* Try running the command from a different PC to see if the issue is specific to one machine.
* Reboot your PC to see if it resolves the issue.

## Example Command
```bash
ssh -i ~/.ssh/id_ed25519 -L 4000:localhost:4000 -L 3000:localhost:3000 root@<ip-address>
```
## Troubleshooting Steps
1. Check if the port is open on the remote system.
2. Try using the `-R` option for reverse tunneling.
3. Consider using `authbind` to allow non-privileged users to access privileged network services.

## Problem: pNode Connection Issue
**@lulu:** 6/14/25, 6:54 PM
I lost access to my Docker container and need to confirm if my pNode is still running.

## Solution
* Check your pNode by logging into it via the SSH command and checking the web GUI for a connection.
* If you have regained SSH access, check if the original pNode setup is missing (no Docker installed, no containers running, etc.).
* If recovery fails, you can reinstall and restore using your backed-up `pnode-keypair.json`.

## Troubleshooting Steps
1. Log into your pNode via SSH and check the web GUI.
2. Check if your node is currently connected on the Xandeum end by contacting the team directly.
3. If you need to reinstall, use your backed-up `pnode-keypair.json` to restore your pNode.

## Problem: Private Docker Image
**@lulu:** 6/19/25, 10:39 AM
I need to restore my pNode from a snapshot, but the Docker image `ghcr.io/xandeum/pnode:latest` is private and requires authentication.

## Solution
* Contact the Xandeum team for the correct image URL or Docker login instructions.
* Note that Docker is not mentioned in the Xandeum documentation, so this may be a separate issue.

## Problem: Verifying pNode Status
**@lulu:** 6/20/25, 5:12 PM
I need to verify if my pNode is still running without interruption after some technical issues.

## Solution
* Log into your pNode and ensure it is correct.
* Go to the `seenodes` web page and check if your wallet is listed.
* Check the latest list of onboarded pNodes in the `devnet-pnode-operations` channel.