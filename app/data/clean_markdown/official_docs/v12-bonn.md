---
original_filename: docs.xandeum.network_v12-bonn_b9f857f0.txt
source: https://docs.xandeum.network/v12-bonn
ingested_at: 2026-01-20
---

## Introduction to v1.2 Bonn
From the outside it looks as if we have jumped from v0.8 Reinheim to v1.2 Bonn. In the background Xandeum has been developing the intervening releases.

## Release History
* v0.9 Bamberg: Improved redundancy statistics for apps and allows tracking of app-requested metrics.
* v1.0 Frankfurt: Now shows redundancy stats and storage volume on a public page, which can be queried by community-developed support and management software.
  * Includes test crash tolerance.
  * An updated XandMiner.
  * An update to the pNode Portal.
  * [https://stats.xandeum.network/](https://stats.xandeum.network/)
* v1.1 Olef: Introduces the ability to repair pages utilizing the power of the pNode network to reliably restore data.

## Mainnet Launch Update – January 2026
Xandeum mainnet launched on December 31, 2025, with the first pNodes coming online on January 1, 2026. As of January 2026, the network is live and stable, currently operating with community pNodes.

## Current Mainnet Access
* Official RPC: Available at `api.mainnet.xandeum.network` (rate-limited).
* Community-operated RPCs: Multiple independent, community-run endpoints are now live or coming online shortly, providing additional access options.

## Upcoming Mainnet Roadmap (Provisional)
* January 2026 (expected): Rollout of STOINC – storage income model where applications pay fees in SOL, distributed proportionally to pNodes.
* February 2026 (expected): Transition XAND staking from Realms DAO to direct on-pNode staking; introduction of bonded pNodes (slashable bond tier for higher rewards and accountability).
* Q3 2026 (expected, by end of September): Activation of Byzantine Fault Tolerance (BFT) for full unstoppable data guarantees, alongside supply/demand-based dynamic storage pricing.

## State of Development Post-Bonn
Bonn (v1.2) marks a major milestone in operational maturity and production readiness for Xandeum's scalable storage layer. This release introduces Crash Fault Tolerance with automated eviction and data replacement for unresponsive pNodes, dedicated pod logging for improved diagnostics, and a full-featured pNode portal that enables secure owner-operator separation through Solana mainnet-signed transactions.

## Core Features
* Crash Fault Tolerance (CFT)
  + Now includes an evict & replace protocol to manage low-performing or unresponsive pNodes and replace their data storage from other pNodes, allowing a pNode to automatically return to the network once it has recovered.
* Pod Dedicated Log Storage
  + Pod now has dedicated log storage.
* pNode Portal
  + A pNode portal has been introduced to support an owner-operator model and is supported through XandMiner. We have implemented a change from Solana devnet to mainnet so that wallets can sign transactions for:
    1. register/update pNode
    2. assign manager
    3. create/update rewards account
    4. register as pNode manager and update manager account details
    5. update pNode manager account

## Summary
Bonn (v1.2) significantly improves network reliability and operational control with automated Crash Fault Tolerance, dedicated logging, and a mainnet-enabled pNode portal supporting owner-operator governance. These advancements deliver self-healing storage, better diagnostics, and secure management, advancing Xandeum toward robust, production-ready mainnet operations in 2026.