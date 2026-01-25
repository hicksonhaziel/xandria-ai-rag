---
original_filename: devnet-supports-1.txt
ingested_at: 2026-01-20
---

## Problem: pNode RPCs are down
**@Don Vicks:** pNode RPCs are down.
**@Ymetro:** The public open node might have gone private or down. Here is a list of public nodes:
```json
"address": "173.212.207.32:9001",
"address": "152.53.236.91:9001",
"address": "62.171.138.27:9001",
"address": "89.123.115.81:9001",
"address": "45.151.122.77:9001",
"address": "161.97.185.116:9001",
"address": "192.190.136.28:9001",
"address": "89.123.115.79:9001",
"address": "154.38.171.140:9001",
"address": "154.38.170.117:9001",
"address": "152.53.155.15:9001",
"address": "45.151.122.60:9001",
"address": "173.249.3.118:9001",
"address": "216.234.134.5:9001",
"address": "161.97.97.41:9001",
"address": "62.171.135.107:9001",
"address": "173.212.220.65:9001",
"address": "192.190.136.38:9001",
"address": "207.244.255.1:9001"
```
Pick a few for redundancy and failover.

## Problem: Atlas repo purpose
**@tobytobias:** What is the Atlas repo for?
No solution provided.

## Problem: pNode credits
**@Starlight:** How to obtain credits earned by a node?
**@Ymetro:** Call `https://podcredits.xandeum.network/api/pods-credits`

## Problem: pNode credits update frequency
**@Hickson.dev:** How often do credits change?
**@Brad|Xandeum-imposter:** Every 30 seconds.

## Problem: pNode uptime calculation
**@Ymetro:** Current uptime calculation might not be accurate.
**@Substance 2.42:** Use raw pRPC data and history graphs.

## Problem: Vercel deployment issues
**@Davethompson:** Having issues deploying on Vercel.
**@Ymetro:** Use environment variables and absolute URLs.
```javascript
const baseUrl = process.env.NEXT_PUBLIC_VERCEL_URL 
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}` 
  : 'http://localhost:3000/';
const res = await fetch(`${baseUrl}/api/data`);
```

## Problem: Getting individual pod information
**@dharmin:** How to get individual pod information?
**@Ymetro:** Use `get-pods-with-stats` and filter the results.

## Problem: Posting deployed links
**@gol.D.roger:** Where to post deployed links?
**@Ymetro:** Post in ⁠💡apps-developers channel.

## Problem: Adding docs to website link
**@gol.D.roger:** Is it fine to add docs to website link?
No solution provided.

## Problem: pNode RPC port
**@Bobby1337:** What is the standard pRPC port for Xandeum pNodes?
**@Ymetro:** Port 6000 is the right port for pRPC.

## Problem: pNode storage used calculation
**@Ninja0x:** How to calculate storage used?
**@Brad|Xandeum-imposter:** Convert `storage_used` field from bytes to MB.
```bash
curl -X POST http://192.190.136.28:6000/rpc \
  -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "method": "get-pods-with-stats",
  "id": 1
}' | jq
```