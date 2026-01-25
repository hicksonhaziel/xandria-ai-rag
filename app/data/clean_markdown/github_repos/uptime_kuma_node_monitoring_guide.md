---
original_filename: uptime_kuma_node_monitoring_guide.md
source: https://github.com/louislam/uptime-kuma
ingested_at: 2026-01-20
---

# Uptime Kuma: Xandeum pNode Monitoring Guide

## Introduction
Uptime Kuma is a self-hosted monitoring tool used to track the availability of Xandeum pods. This guide covers how to monitor the **pRPC API (6000)** and **Gossip (9001)** ports, set up Discord alerts, and troubleshoot common monitoring failures.

## 1. Installation (Ubuntu/Docker)
The most reliable way to run Uptime Kuma alongside your Xandeum node is via Docker.

### Standard Installation
```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
Docker Container Health Monitoring (Advanced)To allow Uptime Kuma to monitor the actual health status of your xandeum-pod container, you must mount the Docker socket:Bashdocker run -d --restart=always \
  -p 3001:3001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v uptime-kuma:/app/data \
  --name uptime-kuma louislam/uptime-kuma:1
2. Monitoring Xandeum PodsOnce installed, access the dashboard at http://<your-ip>:3001.A. Monitoring the pRPC API (TCP)This confirms the Xandeum software is responsive and the API is up.Monitor Type: TCP PortFriendly Name: Xandeum pRPCHostname: 127.0.0.1 (if on same server) or your Public IPPort: 6000Heartbeat Interval: 60 secondsB. Monitoring Gossip (UDP/TCP)This confirms the node can communicate with peers.Monitor Type: TCP PortFriendly Name: Xandeum GossipPort: 9001C. Monitoring via JSON-RPC (Advanced)To verify the pod isn't just "running" but actually "synced":Monitor Type: HTTP(s)URL: http://127.0.0.1:6000/rpcMethod: POSTBody: {"jsonrpc":"2.0","method":"get-version","id":1}Expected Status Code: 2003. Discord Notifications SetupTo receive instant alerts on your phone when your pNode fails:Discord Side:Go to Server Settings > Integrations > Webhooks.Click New Webhook, name it "Node Monitor", and Copy Webhook URL.Uptime Kuma Side:Go to Settings > Notifications > Setup Notification.Type: DiscordDiscord Webhook URL: Paste your URL.Default Enabled: ON (Apply to all monitors).Click Test and Save.4. Common TroubleshootingMonitor reports "DOWN" but Node is "UP"Docker Network: If Uptime Kuma is in a Docker container and the Node is on the host, use host.docker.internal or the actual Public IP instead of 127.0.0.1.Firewall (UFW): Ensure the machine running Kuma is allowed to talk to ports 6000 and 9001.Bashsudo ufw allow from <Kuma-IP> to any port 6000
"Service Unreachable" (DNS Issues)If using a hostname instead of an IP, ensure the container has DNS access.Fix: Add --network="host" to your Docker run command to bypass internal Docker networking issues.Log Truncation & UptimeIf your node crashes during log rotation, Uptime Kuma will catch the downtime. Ensure your logrotate uses copytruncate so the file handle isn't dropped, which can sometimes cause the pod process to hang.Default Configuration SummaryServicePortMonitor TypeImportancepRPC API6000TCPCriticalGossip9001TCPHighDashboard80HTTPOptionalKuma UI3001HTTPManagement
**Next Step:** Since we've covered the docs and monitoring, would you like me to 