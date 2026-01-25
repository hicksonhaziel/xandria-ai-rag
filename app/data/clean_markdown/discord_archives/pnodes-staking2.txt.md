---
original_filename: pnodes-staking2.txt
ingested_at: 2026-01-20
parts: 2
note: Large file - split into multiple sections
---

## Problem: Setting up ChillXand for PNode Management
**@Chill Marketing guy:** Introducing ChillXand, a "set it and forget it" solution for managing pNodes, removing technical headaches and maximizing uptime.

## Problem: Onboarding PNodes
**@S. Kuhlmann:** Onboarding step is not needed for Dutch Auction nodes. 
**@Ymetro:** Registering is different from onboarding. Onboarding is necessary for rewards.

## Problem: PNode Controller
**@Chill Marketing guy:** The controller is a dashboard for quick status checks of pNodes when managed by ChillXand.

## Problem: Upgrading PNodes
**@mrhcon:** Upgraded to Herrenberg, no worries with ChillXand.
**@Chill Marketing guy:** 32 pNodes upgraded to Herrenberg while owners chilled.

## Problem: NFT Boosts and Dutch Auction PNodes
**@mrhcon:** Concerns about selling NFT boosts separately, potentially undervaluing original investments.
**@TSBP:** Suggests gifting a boost NFT to original 300 pNodes that get onboarded.

## Problem: Onboarding Issues
**@Olaf V.:** Onboarding website states "Submissions are closed".
**@csoaita:** Waiting for onboarding to reopen, as mentioned by Bernie.

## Problem: PNode Rewards and STOINC
**@Andr3y11:** No payouts since June.
**@Zedok:** Xandeum keeps telling us we're the best community, but no payouts.

## Problem: Solana Wallet Issues
**@Deleted User:** Solana wallet not letting me unstake Xandeum, transaction reverts.
**@NeoBubba:** Wrong channel, potential blockchain issue with wallet.

## Problem: PNode Performance and DevNet
**@NeoBubba:** Dormant nodes make it hard to run a complete DevNet.
**@Chill Marketing guy:** Let ChillXand manage your pNodes, get them online and earn DevNet rewards.

## Problem: PNode Updates and Software Versions
**@Chill Marketing guy:** 7 pNodes running outdated software versions, updates are necessary for STOINC.
**@Ymetro:** Some nodes not using ChillXand, why not?

## Problem: XAND Price Crash
**@Substance 2.42:** Investigating the cause of the XAND price crash, potential whale activity.

## Problem: Pod Startup Issues
**@G:** Issues with pod startup, Error: Symlinked File not Found : /run/xandeum-pod.
```bash
pod --rpc-ip 127.0.0.1 --keypair ~/.xandeum/keypairs/pnode-keypair.json
```
Anyone know what's missing or a different path to use?

---

## Problem: pNode Registration and Configuration
**@Substance 2.42:** When you dedicate space in GUI (where you created keypair), it will create `/etc/tmpfiles.d/xandeum-pod.conf`, and that will create `/run/xandeum-pod` link that points to created Xandeum "pagefile". So `ls -l /run/xandeum-pod` must show existing file.

## Problem: Upgrading xandminer Software
**@redcali:** In case anybody else has this issue, I ran into a problem upgrading the xandminer software `npm error ENOTEMPTY: directory not empty, rename '/root/xandminer/node_modules/eslint-config-next' -> '/root/xandminer/node_modules/.eslint-config-next-2uijUkP8'`. 
SOLUTION: ran `cd /root/xandminer` and `rm -rf node_modules` to drop the folder and reran the installer with option 2.

## Problem: Accessing pNode Information from Python
**@mark:** I am trying to programmatically access pNode information from Python. I know that XandMiner UI talks to the local pNode daemon to get:
* node status
* segment data
* bucket/FS info
* storage metrics
* heartbeat / uptime
But there is no public documentation showing the daemon’s REST API.
Could you please share:
* The official local daemon API endpoints
* The correct port it runs on
* Whether a public/remote registry API exists for querying all pNodes
* Any JSON schema or examples for interacting with the pNode backend

## Problem: ROI Formula for Running More Than 3 pNodes
**@Manxlanni:** Hi, does anyone know the formula of ROI for running more than 3 pnodes?
**@Substance 2.42:** The formula is: 
`boostedCredits = (pNode1.boostFactor * pNode2.boostFactor * pNode3.boostFactor * ... * pNodeN.boostFactor)^(1/N)`
Where N is the number of pNodes you own.
Example:
For a wallet with 3 pNodes and 100,000 storageCredits:
pNode 1: Boost factor = 1.5 (50% boost)
pNode 2: Boost factor = 1 (no boost)
pNode 3: Boost factor = 2 (100% boost)
`boostedCredits = 100,000 × (1.5 × 1 × 2)^(1/3) ≈ 100,000 × 1.44225 = 144,225`
Adding a 4th pNode with boost factor = 1 (no boost):
`boostedCredits = 100,000 × (1.5 × 1 × 2 × 1)^(1/4) ≈ 100,000 × 1.31607 = 131,607`
Adding a 4th pNode with boost factor = 1.5 (50% boost):
`boostedCredits = 100,000 × (1.5 × 1 × 2 × 1.5)^(1/4) ≈ 100,000 × 1.45648 = 145,648`

## Problem: Calculating STOINC
**@Substance 2.42:** STOINC will be total fees: 
All storage fees (in SOL) collected from sedApps in the epoch × pNode share: The share of fees for pNodes (e.g., 0.94 for 94%) × your boostedCredits calculated above
divided by
total boostedCredits: The sum of boostedCredits across all pNode-owning wallets.
Example: `1000 SOL × 0.94 × 145,648` divided by `36,412,000` boostedCredits of all wallets will result in `3.76 SOL` per epoch.

## Problem: pNode Bonding
**@Zedok:** Looking forward to get more information about "bonding".
**@Substance 2.42:** I added latest video Ep 417 to my simple AI and asked "What is pNode bonding?" - answer was not completely bad... 
**@Zedok:** Let's see if the total amount required for bond is into the millions or tens of millions. Although i doubt it would be in xandeum's interest to make it that high. 

## Problem: Unregistered pNodes
**@Qi:** My wallet has 3 pNodes that are not registered.