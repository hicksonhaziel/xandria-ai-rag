---
original_filename: devnet-validator-operators-2.txt
ingested_at: 2026-01-20
---

## Problem: Unable to Access Solana Home Directory
**@NeoBubba:** Use `cd ~` to get to the Solana home directory.
**@johnc:** Confirmed in the correct directory.

## Problem: Re-running Rustup Commands
**@NeoBubba:** Re-run the "rustup" set of 4 commands again.
**@johnc:** Completed re-running the commands.

## Problem: Rebooting the Server
**@NeoBubba:** Reboot the VPS using `sudo shutdown -r now`, then log back in and start at step 12.
**@johnc:** Rebooted the server, but encountered issues logging back in.

## Problem: Logging Back In After Reboot
**@NeoBubba:** Try pinging the VPS using `ping (ip address here)`.
**@johnc:** Unable to ping the VPS, but eventually logged back in.

## Problem: Compiling and Building
**@NeoBubba:** Try re-compiling and building the project.
**@johnc:** Completed building, but encountered warnings and errors.

## Problem: Network Error and Disconnection
**@NeoBubba:** Check if the build is still running using `top`.
**@johnc:** Build is still running, but encountered a network error and disconnection.

## Problem: Crashed Router
**@NeoBubba:** Reboot the router and server.
**@johnc:** Rebooted the router and server, and logged back in.

## Problem: Build Completion and Validator Restart
**@NeoBubba:** Use `solana config set --url https://api.devnet.xandeum.com:8899/` to set the RPC URL.
**@johnc:** Completed setting the RPC URL, but the validator is not tailing.

## Problem: Tailing the Validator Log
**@Substance 2.42:** Use `tail -f /home/sol/data/logs/solana-validator.log` to tail the log file.
**@johnc:** Successfully tailed the log file.

## Problem: High Skip Rate
**@Substance 2.42:** Check CPUs in `htop`, free space, and internet connectivity to improve the skip rate.
**@johnc:** Investigating the high skip rate.

## Problem: DAO Proposal and Rewards
**@Verena | Xandeum Labs:** Claim rewards using the provided proposal links.
**@mrhcon:** Discussed the 31 locked deposit limit in the DAO.

## Problem: Adding Roles in Channels & Roles
**@Brad|Xandeum-imposter:** Add roles in the Channels & Roles section.
**@mrhcon:** Confirmed the addition of roles.

## Problem: Broken vNode
**@csoaita:** Reported a broken vNode and requested assistance with staking.
**@Brad|Xandeum-imposter:** Investigating the issue with the vNode.