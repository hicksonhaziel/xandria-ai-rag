---
original_filename: docs.xandeum.network_core-concepts_c9c6a7d0.txt
source: https://docs.xandeum.network/core-concepts
ingested_at: 2026-01-20
---

## Introduction to Xandeum
Xandeum is a decentralized storage layer built on Solana, designed to overcome the blockchain's storage limitations by enabling scalable, smart contract-native storage up to exabytes for data-intensive applications like DeFi, NFTs, AI, and big data.

## Key Features
* Scalable Storage Layer: A blockchain-enabled file system that allows Solana programs to store and access massive amounts of data (e.g., terabytes or more) with seamless random access, unlike Solana's limited account-based storage.
* Proof of History Integration: Leverages Solana's PoH for timestamping and ordering storage operations, ensuring efficient, verifiable data management without compromising the base layer's speed.
* Erasure Coding for Redundancy: Data is split into pages, encoded with configurable redundancy (e.g., Reed-Solomon codes), and distributed across nodes to provide fault tolerance and data availability while minimizing storage overhead.
* Cryptographic Proofs (Poke, Peek, Prove): Core primitives for interacting with storage; Poke offloads data to pods, Peek retrieves it on-chain, and Prove verifies integrity using zero-knowledge-like proofs, all wrapped in Solana transactions.
* Decentralized Node Network: Comprises pNodes (provider nodes for actual data storage) and vNodes (validator nodes for supervision), creating a supervised, incentivized ecosystem that scales storage without burdening Solana validators.
* Liquid Staking and DAO Governance: Powered by XAND (governance token) and XandSOL (liquid staking token for SOL), enabling users to stake, earn rewards, and participate in community-driven decisions via the Xandeum DAO.
* Storage Fees in SOL: Fees for storage operations are paid in SOL, distributed to validators, pNodes, and the DAO treasury, fostering economic alignment with the broader Solana ecosystem.

## Investor Perspective
Xandeum offers investment opportunities through its tokens, XAND (governance and utility token) and XandSOL (liquid staking token), with a focus on rewards, governance, and network growth. The model emphasizes community incentives, airdrops, and treasury accrual from fees, positioning it for long-term value in Solana's expanding ecosystem.
* XAND Tokenomics: Fixed supply of 4.015 billion tokens, with allocations for marketing (10%), ecosystem development (10%), community grants (2%), airdrops, and DAO treasury; circulating supply starts low (580 million on day 1) with vesting cliffs to manage inflation and reward long-term holders.
* Governance and Voting Power: XAND holders lock tokens to vote in the DAO, influencing network upgrades, parameter changes (e.g., fees), and treasury spending, (staking commissions, storage transactions) flow to the treasury, creating value accrual for stakers.
* Airdrops: Five planned airdrops (e.g., snapshot-based, with 50% immediate claim and 50% vesting); 
* XandSOL Liquid Staking: Stake SOL to receive XandSOL, which earns XAND rewards through seasonal programs (3-month cycles); multipliers like 10x in early phases (Hyperdrive for <30k SOL staked) boost yields, with real-time accrual and end-of-season claims—staking volume has exceeded 30,000 SOL (over $8M TVL), offering industry-leading APY of around 15%, double that of competitors like Jito and Marinade.
* Raydium Liquidity Provision Opportunities: Investors can provide liquidity to a XandSOL-related pool on Raydium (e.g., SOL-XAND) to earn trading fees and potential farming rewards with high APRs with liquidity amounts reaching $100,000.

## Developer Perspective
Xandeum empowers developers to build and participate in its storage infrastructure, integrating seamlessly with Solana for creating data-heavy dApps. Focus is on running nodes, using protocols for storage access, and contributing to the network for rewards.
* pNodes (Provider Nodes): Decentralized storage nodes responsible for holding encrypted data pages; participate by running hardware/software setups (e.g., via devnet guides), earning SOL fees and XAND rewards for availability and integrity, when possible join wait lists for sales and incentives.
* vNodes (Validator Nodes): Supervisory nodes that cryptographically monitor pNodes using proofs to ensure data redundancy and prevent faults; developers can run vNodes on Solana's devnet/martinet, contributing to consensus and earning commissions from the DAO treasury.
* RPC (Remote Procedure Call): Refers to mechanisms for random access and integrity challenges in storage operations; developers implement RPC in dApps for querying/verifying pNode data off-chain, integrating with Solana RPC endpoints for seamless calls.
* pRPC (Provider RPC): Extension for provider-side handling, possibly physical node-specific protocols for data replication and challenges; participate by configuring pNodes to respond to pRPC requests, ensuring cryptographic supervision and earning rewards for compliance.
* Devnet Participation: Start by running a devnet validator or pNode using official docs; test storage primitives (Poke/Peek/Prove) in Solana programs, with tools for erasure coding and redundancy configuration.
* Building dApps: Use Xandeum-enabled RPC nodes to extend Solana accounts with Web3 storage; developers can create storage-intensive apps (e.g., AI models, big data) and propose grants via DAO for ecosystem funding.
* Rewards and Governance: Earn from storage income (STOINC) programs, with sold-out pNode rounds indicating high demand, a focus on uptime and performance for merit-based incentives.