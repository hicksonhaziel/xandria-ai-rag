---
original_filename: devnet-pnodes-operators-1.txt
ingested_at: 2026-01-20
---

## Problem: Gossip Traffic Flow
**@Ymetro:** Reasons how it keeps the gossip traffic flowing: 
* Outbound-only communication
* Peer-to-peer NAT traversal (hole-punching)
* Fallback to alternative ports/protocols
* Bootstrap via public relays
* Local-network broadcasting
* Stateless nature of gossip

## Problem: Ping Inside Gossip
**@Bhondu:** How the ping inside gossip works. Tried to get ping data but every time it gets timed out. 
**@S. Kuhlmann:** `ss -tlnp | grep 9001` returns nothing on his pnode.

## Problem: pNode Hardening
**@S. Kuhlmann:** There should be a section on how to "harden" the pNode in the docs.

## Problem: Credit Loss
**@mrhcon:** Losing 100+ points from credit score despite Heartbeat working properly. Discovered that after a Big Bang data event, credit loss occurs. 
**@Brad|Xandeum-imposter DM'ing You:** Missing or not responding properly or timely to a data transaction is a -100 in credits, and each heartbeat is a +1.

## Problem: Error Messages
**@mrhcon:** Shared error messages:
```bash
[2026-01-10 11:05:39] ERROR [pod::client:501] - Failed to receive data operation: Failed to deserialize packet : InvalidTagEncoding(111)
[2026-01-10 11:05:39] ERROR [pod::client:802] - Data stream error: Failed to deserialize packet : InvalidTagEncoding(111) - reconnecting streams
[2026-01-09 17:04:15] ERROR [pod::client:660] - Operation PMigrate (ID: 1767996255074000241) failed: Global page number 93 not found in the index.
```
**@Brad|Xandeum-imposter DM'ing You:** These errors may indicate a problem with the xandeum-pages file.

## Problem: Debug Logs
**@mrhcon:** Not getting debug messages with `RUST_LOG=debug`.
**@Brad|Xandeum-imposter DM'ing You:** The correct environment variable is `LOG_LEVEL=debug`.

## Problem: pNode Monitoring
**@Ymetro:** To get push notifications for checking Pod is still running on your pNode to an Uptime Kuma instance:
1. Install Uptime Kuma on a local machine.
2. Add a new monitor with the "Monitor Type": "Push".
3. Copy the script from `pod-check.sh` and replace `your-uptime-kuma-instance` with your Uptime Kuma domain and `<your-id>` with the push monitor ID.
4. Make the script executable with `chmod +x pod-check.sh`.
5. Create a service to run the script automatically after a reboot.

## Problem: Wireguard VPN Connection
**@S. Kuhlmann:** Shared a blog post on setting up a Wireguard VPN connection between pNodes and a local network for heartbeat monitoring and Uptime Kuma.
```bash
https://www.adultintraining.us/post/secure-your-vps-services-with-wireguard-a-complete-guide-to-site-to-site-vpn-with-uptime-kuma-monit
```
**@kryptobiten:** Had issues with Wireguard and switched to Tailscale instead. 

## Problem: pNode Uptime Monitoring
**@Ymetro:** Updated `pod-check.sh` script for pNode uptime monitoring:
```bash
#!/usr/bin/env bash
# ------------------------------------------------------------
# pod-check.sh – lightweight heartbeat sender for Uptime Kuma
# ------------------------------------------------------------

# ----- Configuration -------------------------------------------------
```