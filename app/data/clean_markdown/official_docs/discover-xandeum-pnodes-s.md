---
original_filename: www.xandeum.network_post_discover-xandeum-pnodes-s_834126d2.txt
source: https://www.xandeum.network/post/discover-xandeum-pnodes-solana-storage
ingested_at: 2026-01-20
---

## Introduction to Xandeum pNodes
Xandeum pNodes, or Provider Nodes, are the heart of Xandeum's storage layer on Solana. Solana's great for fast transactions, but validators can't handle huge data loads. Xandeum pNodes fix that by acting as a decentralized "hard drive." They store exabytes of data for dApps in Xandeum Buckets, our file system, keeping Solana speedy and secure.

## How pNodes Work
pNodes use erasure coding to split and spread data across nodes with redundancy. If a node goes down, your data stays safe. It's reliable and simple.

## pNodes and Solana
Running a pNode is easy and fits right into Solana. Here's how it works:
* Data In: dApps send data to pNodes via "poke" commands, wrapped in Solana instructions.
* Storage: Data is sliced, encoded, and stored across pNodes with your chosen redundancy level.
* Data Out: Use "peek" to grab data or "prove" to verify it's untampered.

vNodes (validators with Xandeum software) oversee integrity. Updates like version 0.5 (Ingolstadt) boost speed, and 0.6 (Stuttgart) adds crash-proofing. Tools like XandMiner simplify setup, and Herrenberg shows real-time pNode stats. It's permissionless on mainnet – anyone can join.

## Benefits of Running a pNode
Xandeum pNodes are a win for everyone. Here are the top perks:
* Earn Cash: Devnet offers ~10,000 XAND monthly (locked 12 months). Mainnet brings SOL storage fees.
* Easy Setup: Use a VPS, Ubuntu 24.04+, and our script. No fancy gear needed.
* Early Advantage: Only 300 devnet slots now – early pNode runners get Airdrop 2 points.
* Power Solana: pNodes enable big-data dApps (NFTs, DeFi, AI) by easing validator loads.
* Community: Join Discord for tips and use Herrenberg for staking insights.

## Setting Up Your pNode
Ready to start? Here's how:
* Gear Up: Get Ubuntu 24.04+, 100GB+ storage, stable internet.
* Install: Use our one-click script and register via XandMiner.
* Monitor: Check Herrenberg for pNode stats and rewards.

Visit [xandeum.network/docs](https://xandeum.network/docs) for details. Join our Dutch Auction to grab a spot.