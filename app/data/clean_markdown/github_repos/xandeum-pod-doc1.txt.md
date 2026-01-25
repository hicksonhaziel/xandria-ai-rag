---
original_filename: xandeum_pod_doc1.txt
source: https://github.com/Xandeum/pod-docs
ingested_at: 2026-01-20
---

# Xandeum Pod Documentation v0.4.2
## Quick Start
### Installation
To install the Xandeum pNode, use the following commands:
```bash
sudo apt update
sudo apt install pod
```
### Basic Usage
To start the pNode with default settings (private pRPC), use the following command:
```bash
pod
```
To start the pNode with public pRPC access, use the following command:
```bash
pod --rpc-ip 0.0.0.0
```
To check the version, use the following command:
```bash
pod --version
```
To get help, use the following command:
```bash
pod --help
```
### Test Your Setup
To test your setup, use the following `curl` command:
```bash
curl -X POST http://127.0.0.1:6000/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get-version",
    "id": 1
  }'
```
## What's Included
### pRPC API
The Xandeum pNode includes a complete JSON-RPC 2.0 API for interacting with your pnode. The available methods are:
* `get-version`: Get pnode software version
* `get-stats`: Retrieve comprehensive pnode statistics
* `get-pods`: List known peer pnodes in the network
### CLI Usage
The Xandeum pNode includes a comprehensive command-line reference. The available options are:
* `--rpc-ip`: Configure pRPC server IP binding
* `--entrypoint`: Set bootstrap node for peer discovery
* `--atlas-ip`: Configure Atlas server connection
## Architecture Overview
The Xandeum pNode consists of several key components:
* pRPC Server: JSON-RPC API on port 6000 (configurable IP)
* Stats Dashboard: Web interface on port 80 (localhost only)
* Gossip Protocol: Peer-to-peer communication on port 9001
* Atlas Client: Data streaming connection on port 5000
## Default Configuration
The default configuration is as follows:
| Service | Port | Access | Configurable |
| --- | --- | --- | --- |
| pRPC API | 6000 | Private (127.0.0.1) | IP only |
| Stats Dashboard | 80 | Private (127.0.0.1) | No |
| Gossip Protocol | 9001 | All interfaces | No |
| Atlas Connection | 5000 | Fixed endpoint | No |
The pnode is configured to be secure by default, with the pRPC API being private unless explicitly configured otherwise.