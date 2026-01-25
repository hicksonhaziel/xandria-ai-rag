---
original_filename: devnet.xandeum.network_faucet-repayment_64b64409.txt
source: https://devnet.xandeum.network/faucet-repayment
ingested_at: 2026-01-20
---

## Introduction to Faucet Repayment
The Faucet is used to supply tokens for development and staking on our DevNet. They have no value. When you run a DevNet validator, you earn DevNet Tokens into your vote account. We would appreciate you repaying these back into the faucet so we can keep funding future projects on DevNet! We have 2 wallet accounts for the faucet.

## DevNet Faucet Addresses
> BkFN8AC5aak9bXYxLLyXsUm1QJhbZh6aYEVHidJC3rs7

## DevNet Standard
Run as sol user from the /user/sol directory
1. `su xand`
2. `cd ~`
Check your balance:
```bash
solana balance ~/vote-keypair.json
```
If your withdraw key is stored on the machine, send 1000 to your validator-keypair to pay for vote transactions:
```bash
solana withdraw-from-vote-account --authorized-withdrawer ~/withdraw-keypair.json ~/vote-keypair.json ~/validator-keypair.json 50
```
Send the rest of your DevNet earnings back to the faucet:
```bash
solana withdraw-from-vote-account --authorized-withdrawer withdraw-keypair.json vote-keypair.json BkFN8AC5aak9bXYxLLyXsUm1QJhbZh6aYEVHidJC3rs7 ALL
```

## High Op-Sec Option
If your withdraw key is NOT stored on the machine, then use this. This will require you to input your 12 words (+bip39 passphrase if used).
```bash
solana withdraw-from-vote-account --authorized-withdrawer ASK vote-keypair.json BkFN8AC5aak9bXYxLLyXsUm1QJhbZh6aYEVHidJC3rs7 ALL
```
Recover a keypair from seed phrase to json output file. Bip39 passphrase (if used) will be required after seed phrase is accepted.
```bash
solana-keygen recover -o temporary-key.json
```
Withdraw from vote account using temporary withdraw keyfile and send back to faucet address.
```bash
xandeum withdraw-from-vote-account --authorized-withdrawer temporary-key.json vote-keypair.json BkFN8AC5aak9bXYxLLyXsUm1QJhbZh6aYEVHidJC3rs7 ALL
```