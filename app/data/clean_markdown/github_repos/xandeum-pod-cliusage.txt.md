---
original_filename: xandeum_pod_cliusage.txt
source: https://github.com/Xandeum/pod-docs
ingested_at: 2026-01-20
---

# Xandeum Pod Documentation v0.4.2
## CLI Usage
The Xandeum pNode is a high-performance blockchain node that provides JSON-RPC API, peer-to-peer communication via gossip protocol, and real-time statistics monitoring.

### Basic Usage
#### Start with Default Settings
```bash
pod
```
Starts the pnode with default configuration:
- pRPC server on 127.0.0.1:6000 (private)
- Stats server on 127.0.0.1:80 (private)
- Uses default bootstrap node for peer discovery

#### Check Version
```bash
pod --version
```
Output: `pod 0.4.2`

#### Get Help
```bash
pod --help
```
Shows complete usage information with all options and examples

## Command-Line Arguments
### Options
* `--rpc-ip <IP_ADDRESS>`: Set RPC server IP binding [default: 127.0.0.1 for private]
* `--entrypoint <IP:PORT>`: Bootstrap node for peer discovery [default: 173.212.207.32:9001]
* `--no-entrypoint`: Disable peer discovery (run in isolation)
* `--atlas-ip <IP:PORT>`: Atlas server address for data streaming [default: 95.217.229.171:5000]
* `-h, --help`: Print help
* `-V, --version`: Print version

### Examples
#### Private Access
```bash
pod --rpc-ip 127.0.0.1
```
#### Public Access
```bash
pod --rpc-ip 0.0.0.0
```
#### Bind to Specific Network Interface
```bash
pod --rpc-ip 192.168.1.100
```
#### IPv6 Localhost
```bash
pod --rpc-ip ::1
```
### Security Note
Using `0.0.0.0` makes your pRPC API accessible from any network interface. Only use this if you understand the security implications.

## Common Usage Patterns
* **Private Development Setup**: `pod --no-entrypoint`
* **Public Node**: `pod --rpc-ip 0.0.0.0`
* **Enterprise/Private Network**: `pod --rpc-ip 192.168.1.100 --entrypoint 192.168.1.50:9001 --atlas-ip 192.168.1.10:5000`
* **Local Testing with Custom Atlas**: `pod --atlas-ip 127.0.0.1:5000 --no-entrypoint`

## Port Information
| Service | Default Port | Configurable | Description |
| --- | --- | --- | --- |
| pRPC API | 6000 | IP Only | JSON-RPC API endpoint |
| Stats Dashboard | 80 | ❌ Fixed | Web-based statistics dashboard (localhost only) |
| Gossip Protocol | 9001 | ❌ Fixed | Peer-to-peer communication and bootstrap discovery |
| Atlas Connection | 5000 | ❌ Fixed | Connection to Atlas server for data streaming |

## Firewall Configuration
For public nodes, ensure these ports are accessible:
* Port 6000: pRPC API (if using `--rpc-ip 0.0.0.0`)
* Port 9001: Gossip protocol (always required for peer communication and discovery)
* Port 5000: Atlas connection (outbound to Atlas server)

## Error Handling
### Invalid IP Address
```bash
pod --rpc-ip invalid-ip
```
Error: Invalid IP address 'invalid-ip': invalid IP address syntax

### IP Address Not Available
```bash
pod --rpc-ip 192.168.1.200
```
Error: Cannot bind to IP address 192.168.1.200 on port 6000: Address not available.

### Missing Argument Value
```bash
pod --rpc-ip
```
Error: a value is required for '--rpc-ip <IP_ADDRESS>' but none was supplied

### Unknown Argument
```bash
pod --invalid-option
```
Error: unexpected argument '--invalid-option' found

## Configuration Examples
### Development Environment
```bash
pod --no-entrypoint
```
### Production Public Node
```bash
RUST_LOG=info pod --rpc-ip 0.0.0.0
```
### Private Network Setup
```bash
pod \
  --rpc-ip 10.0.1.100 \
  --entrypoint 10.0.1.50:9001 \
  --atlas-ip 10.0.1.10:5000
```
### Environment Variables
```bash
export RUST_LOG=debug
pod
```
### Systemd Service
```bash
[Unit]
Description=Xandeum Pod System service
After=network.target

[Service]
ExecStart=/usr/bin/pod --rpc-ip 0.0.0.0
Restart=always
User=pod
Environment=NODE_ENV=production
Environment=RUST_LOG=info
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=xandeum-pod

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```bash
sudo systemctl enable pod
sudo systemctl start pod
```
Check status:
```bash
sudo systemctl status pod
```
View logs:
```bash
sudo journalctl -u pod -f
```
## Troubleshooting
### Port Already in Use
```bash
sudo lsof -i :6000
```
Kill process using the port:
```bash
sudo kill -9 <PID>
```
### Network Interface Issues
```bash
ip addr show
```
Test if IP is accessible:
```bash
ping <your-ip>
```
### Peer Discovery Problems
```bash
nc -u 173.212.207.32 9001
```
Check local gossip port:
```bash
sudo netstat -ulnp | grep 9001
```