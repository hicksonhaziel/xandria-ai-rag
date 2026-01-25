---
original_filename: devnet.xandeum.network_onboarding_6e3dee63.txt
source: https://devnet.xandeum.network/onboarding
ingested_at: 2026-01-20
---

## Onboarding Process
Follow all the steps on this page to verify you are ready to onboard your validator. After you have the validator running for at least 1 hour, please follow steps 2-6 to ensure you are ready to onboard and start validating transactions.

## Steps to Onboard
1. Check `htop` to see if your CPU cores are active (meaning validator is running)
2. Check the current Solana slot
3. Run your `mon.sh` script and verify you are above the slot listed in 2
4. Run `catchup.sh` script to verify you are staying in pace with the blockchain...ie 0 slot(s) behind (us:12345 them:12345) and watch for 5 minutes
5. Grab the needed info below and submit onboarding form with your IP address, hostname, Validator ID, and Vote ID

## Finding Validator and Vote Account Pubkeys
Use `sol` user to find your Validator ID Pubkey and Vote Account Pubkey:
```bash
solana-keygen pubkey ~/validator-keypair.json
```
```bash
solana-keygen pubkey ~/vote-keypair.json
```

## Finding Public IP Address
Find your Public IP Address with a suitable method, here are two:
* Using `dig`
* Using `curl`:
```bash
curl https://ipinfo.io/ip/
```

## Submit Onboarding Details
Please take a moment to grab your Public IP address, hostname, Validator Pubkey, and Vote Pubkey. Submit to Xandeum Foundation using the onboarding form with the following details:
> Submit your IP address, hostname, Validator ID, and Vote ID using the provided form. 

## Additional Resources
Check out more Validator Commands for further information. 
Visit the onboarding page: https://devnet.xandeum.network/onboarding