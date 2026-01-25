---
original_filename: support2.txt
ingested_at: 2026-01-20
---

## Problem: Wallet Not Appearing in PNode Eligible List
**@lulu:** Hi, my wallet doesn't appear in the list of pnodes eligible for May payouts.

## Problem: Moving VPS Node to Another Region
**@Ymetro:** Let say I want to move my VPS node to another region, so my pNode's IP address changes, do I need to inform the team by a ticket? And will it keep the same South Era benefits?

## Problem: XANDC to XAND Upgrade Window
**@MikeBaker:** Hi there, when will the next XANDC to XAND upgrade window be please?

## Problem: Wallet Connection Issues
**@Ujjiban:** Pls help for wallet connection I cant open my wallet
**@mrhcon:** Maybe you could actually let people know whats going on...  You can't open your wallet?? Where? What were you trying to do? Did it give you an error?

## Problem: Active Running Clock Resetting
**@nilesh vora:** why does my active running clock on my p node reset it self it has done this twice now
**@Ymetro:** Are you running a node on a local network or on a VPS service? And did you reboot the system?

## Solution: Checking Node Status
**@Ymetro:** You can use the following commands to check if everything is okay and check the interface at http://localhost:3000/
```bash
systemctl status xandminer
systemctl status xandminerd
systemctl status pod
ls -lh /
ls -lh /run
```
**@Ymetro:** If you run `ssh -i ~/.ssh/<your private ssh key> root@<contabo vps ip address> -L 4000:localhost_4000 -L 3000:localhost:3000 -L 80:localhost:80` then you can also check the statistics page on http://localhost/ when pod is running correctly.

## Problem: Port 5000
**@nilesh vora:** What is port 5000?
**@Ymetro:** Port 5000 is needed for communication between pod and the network.

## Solution: Checking Port Status
**@Ymetro:** You can check if it is open with the script that Brad made in: devnet-pnode-operations

## Problem: Claiming XAND Rewards
**@mikev:** Hi, I have found my wallet address in the June devnet pay out list but not sure how to claim my Xand.
**@Zedok:** If nothing has changed since I was running my nodes, rewards are allocated in the DAO. Try: https://app.realms.today/dao/XAND
**@Substance 2.42:** You have to click "EXECUTE" button right below where you found your address. Make sure to have wallet connected in top right corner before that, and some fraction of SOL available.

## Solution: Executing Proposal
**@Substance 2.42:** Yeah, clicking on address in Realms DAO opens the address in Solana Explorer, nothing strange about that, not important. And as Ymetro replied, rewards are NOT going to wallet directly, but they are in DAO "My governance power" locked for one year and you'll have to return then to claim them.

## Problem: Data Allocation
**@mikev:** I don't understand this because on my Xandeum dashboard it shows that I have dedicated 100GB....
**@Substance 2.42:** This is info about your blockchain account, and this "data allocation" has NOTHING to do with pNode. Solana blockchain does not know or care something like pNode exists, completely different thing and it's OK.