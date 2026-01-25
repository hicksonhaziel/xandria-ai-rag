---
original_filename: Voter-stake-registry_md.txt
source: https://github.com/Xandeum/voter-stake-registry
ingested_at: 2026-01-20
---

# Voter Stake Registry
[![source](https://img.shields.io/badge/source-voter--stake--registry-blue)](https://github.com/Xandeum/voter-stake-registry)

## Description
Voter-stake-registry is a voter weight addin for Solana's spl-governance program.

With the addin enabled, the governance realm authority can:
* Control which token mints can be used to vote, and at what scaling factor.
* Claw back locked tokens from user deposits where the user has enabled it.

Users can:
* Deposit and withdraw tokens of the chosen mints to gain voting weight.
* Lock up tokens with different vesting schedules.
* Use their voting weight to vote on spl-governance proposals.

## Development
### Rust
Built and developed using Rust stable (rustc 1.79.0 (129f3b996 2024-06-10))
* Run Rust-based tests: `cargo test-sbf`
* `run-generate-anchor-types.sh` generates the latest anchor types file and writes to `./voter_stake_registry.ts`
* To install the TypeScript client, run: `yarn add @blockworks-foundation/voter-stake-registry-client`

### Node/TypeScript
Built and developed using Node (v16.13.1)
```javascript
import { Provider, Wallet } from '@project-serum/anchor';
import { Connection, Keypair } from '@solana/web3.js';
import { VsrClient } from '@blockworks-foundation/voter-stake-registry-client';

async function main() {
  const options = Provider.defaultOptions();
  const connection = new Connection('https://api.devnet.solana.com', options);
  const wallet = new Wallet(Keypair.generate());
  const provider = new Provider(connection, wallet, options);
  const client = await VsrClient.connect(provider, true);
}
```

## Deployment
Users will likely want to compile their own voter-stake-registry and deploy it to an address they control.
Before compiling, look at:
* `Registrar::voting_mints`: The length of this array defines the number of configurable voting mints. Adjust as needed.

### Devnet
For testing purposes, an instance of voter-stake-registry is deployed on devnet:
* `voter-stake-registry`: `4Q6WW2ouZ6V3iaNm56MTd5n2tnTm4C5fiH8miFHnAFHo`
* `spl-governance master`: `i7BqPFNUvB7yqwVeCRJHrtZVwRsZZNUJTdBm7Vg2cDb`

## Usage Scenarios
### Setup
To start using the addin, make a governance proposal with the spl-governance realm authority to:
1. Deploy an instance of the voter-stake-registry.
2. Create a registrar for the realm with the `CreateRegistrar` instruction.
3. Add voting token mints to the registrar by calling the `ConfigureVotingMint` instruction as often as desired.
4. Call the `SetRealmConfig` instruction on spl-governance to set the voter-weight-addin program id and thereby enable the addin.

### Deposit and Vote Without Lockup
1. Call `CreateVoter` on the addin (first time only). Use the same `voter_authority` that was used for registering with spl-governance.
2. Call `CreateDepositEntry` for the voter with `LockupKind::None` and the token mint for that tokens are to be deposited. (first time only)
3. Call `Deposit` for the voter and same deposit entry id to deposit funds.
4. To vote, call `UpdateVoterWeightRecord` on the addin and then call `CastVote` on spl-governance in the same transaction, passing the voter weight record to both.
5. Withdraw funds with `Withdraw` once proposals have resolved.

### Give Grants of Locked Tokens
1. Ask the recipient for their desired address.
2. Make a proposal to call `Grant` for depositing tokens into a new locked deposit entry for their address. Use a governance that either is the realm authority or the token mint's grant authority.
3. If necessary, later make a proposal to call `Clawback` on their deposit to retrieve all remaining locked tokens.

### Manage Constant Maturity Deposits
Constant maturity deposits are useful when there's a vote weight bonus for locking up tokens:
1. Create a deposit entry of `Constant` lockup type with the chosen number of days.
2. Deposit tokens into it.
3. Use it to vote.
4. If you want access to the tokens again, you need to start the unlocking process by either:
	* Changing the whole deposit entry to `Cliff` with `ResetLockup`.
	* Creating a new `Cliff` deposit entry and transferring some locked tokens from your `Constant` deposit entry over with `InternalTransferLocked`.
5. In both cases, you'll need to wait for the cliff to be reached before being able to access the tokens again.

## Instruction Overview
### Setup
* `CreateRegistrar`: Creates a Registrar account for a governance realm.
* `ConfigureVotingMint`: Enables voting with tokens from a mint and sets the exchange rate for vote weight.

### Usage
* `CreateVoter`: Create a new voter account for a user.
* `CreateDepositEntry`: Create a deposit entry on a voter. A deposit entry is where tokens from a voting mint are deposited, and which may optionally have a lockup period and vesting schedule.
* `Deposit`: Add tokens to a deposit entry.
* `Withdraw`: Remove tokens from a deposit entry, either unlocked or vested.
* `ResetLockup`: Re-lock tokens where the lockup has expired, or increase the duration of the lockup or change the lockup kind.
* `InternalTransferLocked`: Transfer locked tokens from one deposit entry to another. Useful for splitting off a chunk of a "constant" lockup deposit entry that you want to start the unlock process on.
* `InternalTransferUnlocked`: Transfer unlocked tokens from one deposit entry to another. Useful for splitting off a chunk to be locked again in a different deposit entry without having to withdraw and redeposit.
* `UpdateVoterWeightRecord`: Write the current voter weight to the account that spl-governance can read to prepare for voting.
* `CloseDepositEntry`: Close an empty deposit entry, so it can be reused for a different mint or lockup type.
* `CloseVoter`: Close an empty voter, reclaiming rent.

### Special
* `Grant`: As the realm authority or mint's grant authority: create a voter (if needed), create a new deposit and fund it. This instruction is intended for use with DAO proposals.
* `Clawback`: As the clawback authority, claim locked tokens from a voter's deposit entry that has opted-in to clawback.
* `UpdateMaxVoteWeight`: Unfinished instruction for telling spl-governance about the total maximum vote weight.
* `SetTimeOffset`: Debug instruction for advancing time in tests. Not usable.

## License
This code is currently not free to use while in development.

## References
* spl-governance