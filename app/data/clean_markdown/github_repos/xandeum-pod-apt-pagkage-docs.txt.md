---
original_filename: xandeum_pod_apt-pagkage_docs.txt
source: https://github.com/Xandeum/pod-apt-package
ingested_at: 2026-01-20
---

# Xandeum Pod Documentation
## Introduction
This documentation is for **Xandeum Pod v1.2.0**, released on December 31, 2025.

## Quick Start
### Installation
To install the Xandeum Pod, follow these steps:
1. **Access Your Server**: Connect to your Linux server or VPS via SSH:
    ```bash
ssh username@your-server-ip
```
2. **Add the Xandeum Repository**: Install the required packages and add the Xandeum repository:
    ```bash
sudo apt-get install -y apt-transport-https ca-certificates
echo "deb [trusted=yes] https://xandeum.github.io/pod-apt-package/ stable main" | sudo tee /etc/apt/sources.list.d/xandeum-pod.list
sudo apt-get update
```
3. **Install the Pod**:
    ```bash
sudo apt-get install pod
```
4. **Verify Installation**: Check the version:
    ```bash
pod --version
```
5. **Prepare a Keypair**: The pod requires a Solana-format keypair file:
    ```bash
solana-keygen new -o ~/pod-keypair.json
```
    or use an existing keypair.

### Basic Usage
#### Devnet (Default Network)
```bash
pod --keypair ~/pod-keypair.json
pod --keypair ~/pod-keypair.json --rpc-ip 0.0.0.0
pod --gossip
```
#### Trynet (Test Network)
```bash
pod --trynet
pod --trynet --keypair ~/trynet-keypair.json
pod --trynet --gossip
```
#### General Commands
```bash
pod --version
pod --help
```

## Test Your Setup
Verify your pod is running correctly:
```bash
curl -X POST http://127.0.0.1:6000/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get-version",
    "id": 1
  }'
```
Expected response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "version": "0.4.2"
  },
  "id": 1
}
```

## Network Environments
The pod supports two network environments:
### Devnet (Default)
Production-ready network for development:
- Requires valid keypair file
- Atlas: `95.217.229.171:5000`
- Bootstrap: `173.212.207.32:9001`

### Trynet
Experimental test network with simplified setup:
- Auto-generates keypair if not provided
- Atlas: `65.108.233.175:5000`
- Bootstrap: `149.102.137.195:9001`

## What's Included
### pRPC API
Complete JSON-RPC 2.0 API for interacting with your pod:
- **get-version**: Get pod software version
- **get-stats**: Retrieve comprehensive pod statistics
- **get-pods**: List known peer pods in the network

### pNode CLI Usage
Comprehensive command-line reference:
- **--keypair**: Path to Solana keypair file (optional for Trynet)
- **--trynet**: Use Trynet environment with auto-generated keypair
- **--rpc-ip**: Configure pRPC server IP binding
- **--entrypoint**: Set bootstrap node for peer discovery
- **--atlas-ip**: Configure Atlas server connection
- **--gossip**: Display network peers and exit
- **--log**: Write logs to a file

## Architecture Overview
The Xandeum Pod consists of several key components:
- **Keypair Identity**: Cryptographic identity for node authentication
- **pRPC Server**: JSON-RPC API on port 6000 (configurable IP)
- **Stats Dashboard**: Web interface on port 80 (localhost only)
- **Gossip Protocol**: Peer-to-peer communication on port 9001
- **Atlas Client**: Data streaming connection on port 5000 with 60-second idle timeout

### Keypair Management
The pod uses Solana-format keypairs for:
- Node identity on the network
- Signing heartbeat messages
- Authenticating with peers
- Future transaction signing capabilities
- Maintaining identity across reconnections

### Connection Management
The pod maintains persistent connections to the Atlas server using the QUIC protocol:
- **Idle Timeout**: 60 seconds - connections are closed after 60 seconds of inactivity
- **Auto-Reconnect**: The pod automatically reconnects when needed
- **Identity Preservation**: Your node's keypair identity is preserved across all reconnections

## Default Configuration
| Service | Port | Access | Configurable |
|---------|------|--------|-------------|
| pRPC API | 6000 | Private (127.0.0.1) | IP only |
| Stats Dashboard | 80 | Private (127.0.0.1) | No |
| Gossip Protocol | 9001 | All interfaces | No |
| Atlas Connection | 5000 | Fixed endpoint | No |