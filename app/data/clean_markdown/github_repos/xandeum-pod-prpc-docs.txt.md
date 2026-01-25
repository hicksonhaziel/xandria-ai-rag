---
original_filename: xandeum_pod_prpc_docs.txt
source: https://github.com/Xandeum/pod-docs
ingested_at: 2026-01-20
---

# Xandeum Pod Documentation v0.4.2
## pRPC API
The Xandeum pNode pRPC API uses JSON-RPC 2.0 protocol over HTTP POST requests. All requests should be sent to the `/prpc` endpoint.

### Base URL
The base URL for the pRPC API is:
```
http://<pnode-ip>:6000/rpc
```
Default: `http://127.0.0.1:6000/rpc` (private)

## Network Architecture
The pnode uses several network ports for different services:
* Port 6000: pRPC API server (configurable IP binding)
* Port 80: Statistics dashboard (localhost only)
* Port 9001: Gossip protocol for peer discovery and communication
* Port 5000: Atlas server connection for data streaming (fixed endpoint)

## Available Methods
### get-version
Returns the current version of the pnode software.

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "get-version",
  "id": 1
}
```
#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "version": "1.0.0"
  },
  "id": 1
}
```
#### cURL Example
```bash
curl -X POST http://127.0.0.1:6000/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get-version",
    "id": 1
  }'
```
## Error Handling
All errors follow the JSON-RPC 2.0 specification and include standard error codes.

### Method Not Found
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```
### Internal Error
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal error"
  },
  "id": 1
}
```
### Standard Error Codes
| Code | Message | Description |
| --- | --- | --- |
| -32601 | Method not found | The requested method does not exist |
| -32603 | Internal error | Server encountered an internal error |

## Integration Examples
### Python Example
```python
import requests
import json

def call_prpc(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    if params:
        payload["params"] = params

    response = requests.post(
        "http://127.0.0.1:6000/rpc",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    return response.json()

# Get version
version = call_prpc("get-version")
print(f"pNode version: {version['result']['version']}")

# Get stats
stats = call_prpc("get-stats")
print(f"CPU usage: {stats['result']['stats']['cpu_percent']}%")
```
### JavaScript/Node.js Example
```javascript
const fetch = require('node-fetch');

async function callPRPC(method, params = null) {
  const payload = {
    jsonrpc: "2.0",
    method: method,
    id: 1
  };
  if (params) payload.params = params;

  const response = await fetch('http://127.0.0.1:6000/rpc', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  return await response.json();
}

// Usage
(async () => {
  const version = await callPRPC('get-version');
  console.log(`pNode version: ${version.result.version}`);

  const stats = await callPRPC('get-stats');
  console.log(`Uptime: ${stats.result.stats.uptime} seconds`);
})();
```
### Bash/curl Example
```bash
#!/bin/bash

PRPC_URL="http://127.0.0.1:6000/rpc"

# Function to call pRPC
call_prpc() {
  local method=$1
  curl -s -X POST "$PRPC_URL" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"$method\",\"id\":1}"
}

# Get version
echo "Getting version..."
call_prpc "get-version" | jq '.result.version'

# Get stats
echo "Getting stats..."
call_prpc "get-stats" | jq '.result.stats.cpu_percent'
```
## Installation
Install the pod via apt: `sudo apt install pod`

## Rate Limiting
There are currently no rate limits on the pRPC API, but be mindful of resource usage when making frequent requests.

## Security
When using `--rpc-ip 0.0.0.0`, your pRPC API will be accessible from any network interface. Ensure proper firewall rules are in place.