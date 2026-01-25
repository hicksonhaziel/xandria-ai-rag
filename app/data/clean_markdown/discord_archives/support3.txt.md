---
original_filename: support3.txt
ingested_at: 2026-01-20
parts: 2
note: Large file - split into multiple sections
---

## Problem: Claiming pNode Xand Rewards
**@Ymetro:** 9/7/25, 4:03 PM
To claim pNode Xand rewards, search for "pNode" in the DAO proposals, click on the result, open the "Instructions" button, and search for your address using Ctrl + F. Make sure to check both instruction lists if the payout is split into two parts.

## Problem: Claiming pNode Xand Rewards
**@Substance 2.42:** 9/7/25, 4:35 PM
To find your rewards, search for your main wallet address, not the pNode address. You can find your rewards in the "June 2025 DevNet pNode payments - Part 2" DAO proposal.

## Problem: Claiming pNode Xand Rewards
**@mikev:** 9/10/25, 9:27 AM
To claim rewards, go to the DAO, find the proposal for the month you're looking for, click on "Instructions", and search for your wallet address. Then, click on the "Execute" button and confirm the transaction in your wallet.

## Problem: pNode Storage Space Issue
**@apreston100:** 9/11/25, 8:08 PM
If you're experiencing a "no more space to dedicate" issue, try restarting the pod with `systemctl restart pod` and then dedicate the amount you want on the storage management page.

## Problem: pNode Storage Space Issue
**@Ymetro:** 9/11/25, 9:07 PM
If the issue persists, try running the following commands:
```bash
fallocate -l 10G /xandeum-pages
systemctl daemon-reload
systemctl restart pod
```
## Problem: Transferring XANDC to XAND
**@minhas01:** 11/10/25, 2:27 PM
Currently, it's not possible to transfer XANDC to XAND as the window has closed. You'll need to wait for the next window.

## Problem: Onboarding a pNode
**@kryptobiten:** 11/20/25, 5:59 PM
To onboard a pNode, use the link: https://pnode-onboarding.paperform.co/

## Problem: pNode Storage Limit
**@kryptobiten:** 11/21/25, 12:55 PM
The pNode storage limit is 17.6TB. If you're experiencing issues with dedicating more space, try checking the storage usage and freeing up space if necessary.

## Problem: Sending Data to a pNode
**@taiwokassim:** 12/5/25, 6:52 PM
To send data to a pNode, use the Xandeum GitHub repository "xandeum-web3.js" and the API calls or JSON-RPC methods provided.

## Problem: Getting pNode Info
**@Pratik:** 12/6/25, 9:53 AM
To get pNode info, use the `devnet-pnode-operations` channel and learn about the pRPC's. You can also use the `getGossipNodes` method to retrieve information about the nodes.

## Problem: Public pRPC Endpoint
**@codeM:** 12/6/25, 10:48 AM
There is no public pRPC endpoint. You need to run your pNode on a VM and use the pRPC's to get the information you need.

## Problem: pNode Setup Guide
**@Brad|Xandeum-imposter DM'ing You:** 12/10/25, 11:08 PM
The Xandeum pNode setup guide can be found at: https://docs.xandeum.network/xandeum-pnode-setup-guide

## Problem: Endpoint Error
**@Bobby1337:** 12/16/25, 8:07 AM
If you're experiencing an endpoint error, check the API documentation and make sure you're using the correct endpoint.

## Problem: Access to pRPC
**@Ndii_Ekanem:** 12/16/25, 2:26 PM
Access to the pRPC is limited. You need to go to the `devnet-developer-support` channel to get more information.

## Problem: Unstaking Xand from DAO
**@Mani:** 12/30/25, 12:25 AM
If you're having trouble unstaking your Xand from the DAO, try checking for any errors or issues with your wallet or the DAO interface.

## Problem: Claiming Staking Rewards
**@Digital Energy:** 1/3/26, 8:20 PM
If you're having trouble claiming your staking rewards, try using a different wallet or checking for any issues with the reward claim process.

## Problem: Using XANDSOL
**@Zedok:** 1/12/26, 3:08 PM
If you're unsure about how to use your XANDSOL, try checking the FAQ section on the Xandeum website or asking for help in the community.

---

## Problem: Understanding XANDSOL Liquidity and Rewards
**@Zedok:** Well it provides liquidity and it gives rewards for it in form of XAND and SOL... and you can "unstake" that liquidity by selling it to SOL again or something else.

## Problem: Converting XANDSOL to SOL
**@Ymetro:** So I get less in XANDSOL than the SOL i bought it with. I can see on the xandsol page how much xandsol I have but is there a way to see how much SOL this corresponds to? Also, if I sell, will I get back the portion of SOL I lost initially?

## Problem: Locating SOL Rewards
**@Zedok:** Here is another daft thing, I can see my XAND rewards, but where do I find my SOL rewards? 
The answer is: Those rewards are then cleverly woven into the price of xandSOL itself. This means the value of your xandSOL steadily increases over time, reflecting your accumulated rewards.
When you finally decide to unstake your xandSOL and head back to planet SOL, you'll receive an amount of SOL that reflects the increased value of xandSOL, essentially giving you your rewards all at once!