---
original_filename: support6.txt
ingested_at: 2026-01-20
---

## Problem: Monitoring pNode Status
**@Substance 2.42:** 5/15/25, 7:51 PM
Tried online port scanner, but ports 3000 and 4000 don't respond. 
**@apreston100:** 5/15/25, 8:02 PM
Used Terminal app on macOS desktop and Termius app on iPhone IOS to monitor a vNode. 
**@Ymetro:** 5/16/25, 12:08 AM
Considered using Uptime Kuma to monitor 4000 TCP port on remote IP address.

## Solution: Using Uptime Kuma
**@Ymetro:** 5/16/25, 3:50 AM
To monitor the status of two services (xandminer and xandminerd) on a remote Linux VPS:
1. Add a shell script (`check_xandminer_status.sh`) to check if services are running.
2. Add a Python HTTP server (`xandminer_status_server.py`) to publish the response over the internet.
3. Add a systemd service file (`xandminer_server_status.service`) to ensure the Python server and script start at each system boot.
4. Set up a local running Uptime Kuma instance to check the server at `http://<ipaddress>:8080/check_services` every 60 seconds.

## Problem: Daemon Online Status
**@apreston100:** 5/16/25, 8:50 PM
Is it necessary for `http://localhost:3000/` to have the Daemon Online permanently?
**@Substance 2.42:** 5/16/25, 9:21 PM
The GUI itself (3000) and daemon (4000) work only while ssh tunnel for given port is active.

## Solution: Understanding Daemon Status
**@Ymetro:** 5/16/25, 11:42 PM
The GUI and daemon apps keep running on the server. The 2 ports are only for administrative access control. 
The recommendation is to disconnect whenever finished making adjustments.

## Problem: Converting XANDC to XAND
**@ocd.andy:** 5/18/25, 1:07 PM
Trying to convert XANDC to XAND through claim #1 on `upgrade.xandeum.network`.
**@Zedok:** 5/18/25, 1:09 PM
The next conversion window will be announced.

## Problem: Onboarding pNode
**@jazzyack:** 5/24/25, 12:14 AM
Trying to ensure not missing any steps for onboarding pNode.
**@Zedok:** 5/24/25, 7:51 AM
Founders nodes have generated tokens which can be collected at `https://upgrade.xandeum.network/`.

## Problem: SSH Connection Issue
**@Ymetro:** 5/28/25, 10:11 AM
Getting a `bind [127.0.0.1]:3000/4000: Permission denied` error when trying to connect to pNode.
**@mrhcon:** 5/28/25, 10:26 AM
Please provide the full command being used to connect.

## Solution: Resolving SSH Connection Issue
**@Ymetro:** 5/28/25, 10:32 AM
Using `ssh -i ~/.ssh/id_ed25519 -L 4000:localhost:4000 -L 3000:localhost:3000 root@<ip-address>`.
**@mrhcon:** 5/28/25, 10:35 AM
Run the command on a PC (not the pNode) and access `http://localhost:3000/` via the same machine's browser.

## Problem: Security Issue Reporting
**@grinku0x:** 5/29/25, 8:45 PM
Want to report a security issue and inquire about the responsible disclosure process and potential rewards.
**@Ymetro:** 5/29/25, 9:22 PM
To contact the team directly, open a support ticket at `⁠🎫open-a-ticket`.