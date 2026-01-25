---
original_filename: devnet-supports-2.txt
ingested_at: 2026-01-20
---

## Problem: Finding pRPC Endpoints
**@Desh:** Can anyone pls point me to the pRPC endpoints?
**@Ymetro:** Sure: devnet-developer-support

## Problem: Endpoint for Stacking Score
**@BarriePotter:** Is there any endpoint for the stacking score for a pnode? Or rpc method?
**@Ymetro:** If you mean Storage Credit score then call the address at the bottom of devnet-developer-support

## Problem: API Abuse
**@Substance 2.42:** So, XanDash, XandeumCollector... will you continue trying to abuse my site, or was it enough already?
**@Bhondu:** Sorry ser, I'll remove the api. Rpc.pchednode. Wasn't aware of the site is yours. I was not trying to abuse anything it was unintentional.

## Problem: Historical Data and Response Time
**@Bhondu:** Is there any way I can get the nodes historical data and response time?
**@Substance 2.42:** No problem, thank you for improving my security settings. As for historical data, they are not available from Xandeum, have to store on your side.

## Problem: Uptime in get-stats
**@tobytobias:** @Brad|Xandeum-imposter DM'ing You uptime in "get-stats" is milli-seconds, right?
```javascript
{
  "status": "success",
  "data": {
    "active_streams": 2,
    "cpu_percent": 1.9900497198104858,
    "current_index": 0,
    "file_size": 104857600,
    "last_updated": 0,
    "packets_received": 10060552,
    "packets_sent": 11658263,
    "ram_total": 4115349504,
    "ram_used": 1220251648,
    "total_bytes": 0,
    "total_pages": 0,
    "uptime": 330117
  }
}
```

## Problem: Public Nodes List
**@Ymetro:** In the meantime (while the devs are upgrading and testing) - here's a list of v0.8.0 nodes that are public:
* 173.212.207.32:9001
* 45.151.122.77:9001
* ...
To get a fresh list yourself use:
```bash
curl -s -X POST http://89.123.115.81:6000/rpc \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"get-pods-with-stats","id":1}' |
# Turn the top‑level array into one compact line per pod
jq -c '.result.pods[]' |
# Keep only pods whose version is 0.8.0
grep -i '"version":"0\.8\.0"' |
# From those, keep only the ones that are public
grep -i '"is_public": *true' |
# Pull out just the address field
grep -o '"address":"[^"]*"' |
cut -d'"' -f4 |
tee /dev/tty |
wc -l | awk '{print "Total public nodes (version 0.8.0):", $1}'
```

## Problem: Pod Credits Reset
**@Skipp:** posted a screenshot of XDOrb in ⁠💡apps-developers. I essentially wanted to ask, were pod credits resetted twice today?
**@mrhcon:** Yes. I experienced the same and the top earner does appear at the time of writing this to be 264

## Problem: API Changes and Documentation
**@John | WAGISDev:** Okay...I have held my tongue for a bit here, but I am going to say this. Coming from a background of moving fast and breaking things with big projects, I can appreciate a bit of that happening when you are NOT in production or begging devs to build things you need to grow the ecosystem.
* 1 work week for any API changes to be made when you have this large of a group trying to develop along side of you filling in gaps
* Updated documentation ahead of the change or at least released at the same time as the change
* Documentation that mirrors the realities
* Updated documentation for the mainnet RPC API or in absence of that, code for the RPC published in GitHub.
* A list of public RPCs to be used for development

## Problem: Detecting Network Type
**@Ymetro:** @Brad|Xandeum-imposter DM'ing You how can the devs get info on which net the pNode is running, devnet or mainnet? As get-pods-with-stats RPC results don't mention this.
**@NeoBubba:** They are 2 different networks, using 2 different API's. You will only get the nodes that are on that network.

## Problem: Mapping pNode Identity to Rewards Wallet
**@Hickson.dev:** building xandria an analytics platform for xandeum Pnodes and I'm stuck on one thing: Since the get-stats pRPC call doesn't return the Owner/Manager wallet address, is there an official on-chain registry or a specific RPC method to map a pNode Identity Pubkey to the Rewards Wallet?
**@mrhcon:** Multipliers are not all NFT's yet and thus not attached to the wallets... Some are (titan, cricket, etc) and some are not (deep south, etc).