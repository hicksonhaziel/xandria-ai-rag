---
original_filename: xandeum.network_stoinc_2872820e.txt
source: https://xandeum.network/stoinc
ingested_at: 2026-01-20
---

## Introduction to STOINC and Rewards
Xandeum Storage Income (STOINC) and Rewards Overview explains how to earn Rewards and Storage Income by participating in the Xandeum Devnet.

## Rewards Program
The Rewards Program supports those who help keep the Xandeum Devnet running smoothly. Rewards are paid in locked XAND tokens and are funded by the Xandeum Foundation.

* Validator Node Operators: Earn 10,000 XAND per month for running a validator node.
* pNode Operators: Earn 10,000 XAND per month for running a pNode.
* Discord Moderators: Earn 40,000 XAND per month for moderating our Discord community.

## Storage Income (STOINC)
STOINC (Storage Income) is the revenue earned by running pNodes, funded by fees from sedApps (storage-enabled dApps).

### STOINC Distribution
Fees from sedApps are split as follows:
* 94% goes to pNode operators.
* 3% goes to the XAND DAO.
* 3% goes to Xandeum Preferred Investors.

### How STOINC is Calculated
Your STOINC depends on storageCredits, calculated every epoch (~2 days) based on four factors:
1. Number of pNodes: Owning more pNodes multiplies your rewards.
2. Storage Space: More storage capacity directly increases rewards.
3. Performance Score: A score (0 to 1) based on your pNode’s reliability and performance.
4. Stake: The amount of XAND you stake influences rewards proportionally.

> Important: If any factor is 0 in an epoch, you earn no rewards for that epoch.

## Boost Factors
Boost factors increase your storageCredits, boosting your STOINC. Each pNode has a boost factor (1 or higher), and the overall boost is calculated using a geometric mean if you own multiple pNodes.

### Example
For a wallet with 3 pNodes and 100,000 storageCredits:
* pNode 1: Boost factor = 1.5 (50% boost)
* pNode 2: Boost factor = 1 (no boost)
* pNode 3: Boost factor = 2 (100% boost)

boostedCredits = 100,000 × (1.5 × 1 × 2)^(1/3) ≈ 100,000 × 1.44225 = 144,225

### Ways to Earn Boost Factors
Boost factors come from NFTs or pNode purchase eras:
#### NFTs
* XENO NFT: 1.1 (10% boost)
* Titan NFT: 11 (1,000% boost)
* Dragon NFT: 4 (300% boost)
* Coyote NFT: 2.5 (150% boost)
* Rabbit NFT: 1.5 (50% boost)
* Cricket NFT: 1.1 (10% boost)

#### pNode Purchase Eras
* DeepSouth Era: 16 (1,500% boost)
* South Era: 10 (900% boost)
* Main Era: 7 (600% boost)
* Coal Era: 3.5 (250% boost)
* Central Era: 2 (100% boost)
* North Era: 1.25 (25% boost)

## Final STOINC Calculation
Your STOINC for an epoch is calculated as:
Where:
* total fees: All storage fees (in SOL) collected from sedApps in the epoch.
* pNode share: The share of fees for pNodes (e.g., 0.94 for 94%).
* total boostedCredits: The sum of boostedCredits across all pNode-owning wallets.

## Key Takeaways
* Rewards (locked XAND) are paid to validator nodes, pNode operators, and Discord moderators, funded by the Xandeum Foundation.
* STOINC (in SOL) comes from sedApp fees and is distributed to pNode operators based on the STODIST formula.
* Storage Credits depend on the number of pNodes, storage space, performance score, and stake.
* Boost Factors from NFTs or early pNode purchases can significantly increase your earnings.