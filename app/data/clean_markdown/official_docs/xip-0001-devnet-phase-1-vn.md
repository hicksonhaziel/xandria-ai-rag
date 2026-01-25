---
original_filename: forum.xandeum.network_t_xip-0001-devnet-phase-1-vn_a46f9547.txt
source: https://forum.xandeum.network/t/xip-0001-devnet-phase-1-vnodes/143
ingested_at: 2026-01-20
---

## XIP-0001: Devnet Phase 1, vNodes
XIP: Incentivized Devnet, Part 1: vNodes

Type: Non-Executable (Multiple-Choice)

Choices:
* Yes (approve the incentivized devnet vNode plan)
* No (reject this proposal)

### Proposal Description
Summary

We propose to launch an incentivized devnet to support Xandeum’s development and community-building efforts. This devnet will serve as a testing ground for intermediate releases and provide valuable feedback before mainnet. In this first phase, we focus on incentivizing vNode (validator node) operators, ensuring they contribute to a stable, high-performing devnet. Subsequent phases will address pNodes (storage nodes) and RPC nodes (Dock and CachedAccess providers).

### Context

Xandeum aims to build a scalable, blockchain-grade storage layer for Solana and potentially Ethereum EVM-based smart contract platforms, integrated with a side network of Pods, Atlas indexing, and Dock logic. As we iterate on our technology, we need a stable reference network—the devnet—to validate our assumptions, test intermediate code changes, and foster a community of skilled operators who understand the platform’s vision.

### Goals
* Establish a devnet from December 30, 2024, until June 30, 2025, running modified Agave clients as vNodes.
* Provide performance-based incentives to encourage stable, efficient validation.
* Begin building a dedicated community of node operators who will play key roles as we transition toward testnet and mainnet.
* Lay the foundation for integrating pNodes and RPC nodes in subsequent proposals.

### Details of the vNode Incentivization
1. **Devnet Timeline**
	* Start: December 30, 2024
	* End: June 30, 2025
2. **Staking and Performance Requirement**
	* Each vNode operator will receive a 10,000 SOL (Xandeum devnet SOL) stake account from the Xandeum Foundation.
	* The validator must maintain performance. Performance is measured by the monthly average staking rewards relative to the top 3 best-earning validators.
	* Threshold: At least 85% of the top-3 average staking rewards.
	* Incentives:
		+ Meeting the threshold earns the full monthly incentive.
		+ Falling below reduces incentives proportionally. Example: Achieving 42.5% of the top-3 average results in 50% of the monthly incentives.
3. **Incentives**
	* Base Incentive: 10,000 XAND per month (locked for 12 months in the DAO before they can be claimed).
	* Incentives will be paid out of the Community Building category of the DAO treasury.
	* Participants active by January 15, 2025, will receive full compensation for January, regardless of performance.
4. **Hardware Recommendations for vNodes**
	* Minimum: 8 vCPUs/threads, 32GB RAM, 500GB SSD storage, and 10 Mbit/s upload/download bandwidth.
	* These are recommendations only—performance is the ultimate criterion.
	* VPS (Virtual Private Servers) are allowed and expected to meet cluster performance requirements. Participants may choose their provider and specifications.
5. **Participant Requirements**
	* Capacity: Aiming for at least 35, but no more than 40 devnet vNodes. Onboarding will close once 40 nodes are online.
	* KYC: Participants must complete Know Your Customer (KYC) verification, including:
		+ Name, address, date of birth.
		+ $1 credit card transaction (Antsle, Inc. will process on behalf of Xandeum Foundation).
		+ ID verification via an external provider chosen by Antsle, Inc.
	* Restrictions:
		+ Maximum of 1 incentivized devnet vNode per participant.
		+ Participants bear all expenses for hardware, hosting, connectivity, operations, etc.

### Rationale
Linking incentives to performance ensures a healthy devnet and provides realistic feedback on validator behavior.
Locking incentives for 12 months aligns operators with the project’s long-term vision.

### Conclusion
Approving this proposal sets the stage for a robust devnet, staffed by engaged and competent validators. This incentivized environment will accelerate development, improve code quality, and foster a loyal community, ultimately benefiting Xandeum’s journey toward a storage-enabled, blockchain-grade solution.