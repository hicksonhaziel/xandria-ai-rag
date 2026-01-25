---
original_filename: support4.txt
ingested_at: 2026-01-20
parts: 2
note: Large file - split into multiple sections
---

## Problem: Unable to Open a Ticket
**@mikev:** How do I open a ticket? I can see options like general and support-questions but there's no open-a-ticket option
**@mrhcon:** Go to the top and make sure you have the right roles selected. Once you have them, you will be able to open a ticket.

## Problem: Ledger Issue with Unstaking Liquid XandSol
**@mcpisik:** Can't unstake xandsol with ledger. Tried in Phantom and Solflare. Just says to ensure blind signing is enabled etc (Which it is)
**@NeoBubba:** Sometimes the first tweet that you try makes you go through the login process and then seems to "flake out" and do nothing, however when I go check it has gone through even though it didn't show it.
**@mcpisik:** My solution was to not use Chrome or Firefox. Installing brave and phantom was the combo that allowed Ledger to connect and transact.

## Problem: Scam Ticket
**@mcpisik:** I had a ticket opened for me maybe by MrKitjan. Is it legit? Name is not marked as part of the team.
**@NeoBubba:** NO! Send screenshot to ⁠⛔scam-lookout please 🙏

## Problem: No Routes Found on Jupiter and Raydium
**@mikev:** Hi, I want to swop a small portion of my XandSol to Sol but getting 'no routes found' on both Jupiter and Raydium. Any suggestions?
**@Substance 2.42:** Seems OK for me (Jupiter swap settings "auto", for amounts ~ 1000 SOL, not for 10000 SOL), but if you staked SOL to XandSOL, perhaps unstake is better route?

## Problem: Unable to Unstake XandSol
**@mikev:** When I try to unstake the XandSol it's asking me to connect my Ledger as the wallet connected is my Phantom Ledger account.
**@agregersen:** Check on your ledger device to make sure you okayed blind signing, it has bit my tail a few times.

## Problem: XandSol Price Not Updating in Phantom
**@Fox46:** looks like xandSOL went to 0 in my phantom wallet. Am I missing something?
**@Substance 2.42:** Don't worry about that, Phantom just sometimes does not know the price, but in other places (Solflare, Jupiter...) it's displayed correctly.

## Problem: Claiming Vested Tokens
**@taojiang:** How to claim vested tokens?
**@NeoBubba:** I would suggest ⁠🎫open-a-ticket and discuss this problem directly with the Xandeum team.

## Problem: Running a pNode on Raspberry Pi
**@kryptobiten:** I would like to know if it's possible to run a pnode on raspberry pi?
**@Substance 2.42:** This was asked before but nobody tried it - try and let us know.

## Problem: pNode Storage Not Detected
**@Ymetro:** Hi. I'm running a pNode setup on Debian 12, but the GUI webpage says it can't find a drive, while I have a partition setup for this.
**@Substance 2.42:** I am not from team, but based on index.tsx and helpers.js source files, the code seems to parse all disks in system... so I guess it should see them, no matter the filesystem.
```bash
sudo apt-mark unhold liblzma5
sudo apt update
sudo apt upgrade
sudo apt install liblzma5=5.6.3-1+b1
sudo apt --fix-broken install
```
**@Ymetro:** I'll give it a shot.

## Problem: Converting XANDC to XAND
**@kezla:** I've been absent with my 97 yo dad in hospital for a month....then away. Timing is off to be catching the Xandeum explosion (woohoo team XANDEUM) but trying to catch up now. Forgive me for asking potentially redundant questions. With 58 hour window left, I've got XANDC to convert to XAND and on the link it no longer shows a Phantom Wallet (only Solflare and Alpha) so what should I do please?
**@Zedok:** Do you have the phantom extension installed on your browser?
**@kezla:** Hi @Zedok - yes, Phantom app is pinned as an extension in Brave browser
**@Zedok:** I can only suggest trying another browser, or raise a ⁠🎫open-a-ticket. Do not reply to any direct message (DM). SCAMMERS.

---

## Problem: Disk Detection Issue
**@Ymetro:** 3/19/25, 8:42 PM - Got it running in WSL Debian on a Windows 11 machine. And it detects 1 drive. Probably a virtual from Docker itself, because it is bigger than my actual free space. 
**@kezla:** Not that I am aware of, should work on both.

## Problem: Unable to Close Resolved Ticket and VIP Discount Code Issue
**@NeoBubba:** 3/20/25, 4:33 AM - Can't `/close` or `/closerequest` my OPEN resolved ticket. And I have a new support query: I have not received my VIP discount code to buy pNodes.

## Problem: Disk Detection with Different Kernels
**@Ymetro:** 3/23/25, 7:11 PM - Resized my root partition to maximum possible and installed Ubuntu 22.04.5 LTS, but still no disks found.
**@Ymetro:** 3/24/25, 2:13 AM - So it seems a `/home` partition doesn't take, and the other partitions are available if the kernel is 6.1 (in Debian Bookworm), while 6.8 (in Ubuntu 22.04.5 LTS) does not see any drives.
**@Substance 2.42:** I update daily, but at the moment: 
```bash
6.1.0-32-arm64
6.1.0-32-cloud-amd64
```
**@Substance 2.42:** Btw, I can see in `helpers.js` source that it lists disk using:
```bash
lsblk -o NAME,SIZE,FSUSED,FSUSE%,RO,TYPE,MOUNTPOINTS --json
```
It looks for:
```javascript
device.type === 'disk' || device.type === 'part'
```
**@Substance 2.42:** Also, it does check OS, what is output of this for you? (Linux or Darwin)
```javascript
node -e "console.log(require('os').platform())"
```
(or `uname -s`)

## Problem: pNode Installation on Proxmox Server
**@Dean C:** 3/28/25, 12:19 AM - Hi guys, I'm trying to install a pnode on my local Proxmox server Version 8.3.5. I have installed a Ubuntu LXC container Version 22.04. I run the `install.sh` OK, but get lots of warnings about deprecated packages & unnecessary dependency, but I do get the "Setup completed successfully!". I can run `curl http://localhost:3000/` locally on the LXC successfully. But if I run `curl http://192.168.x.x:3000/` from another VM or my local network. The connection is refused... The Firewall status on the VE host is disabled/running. The Firewall on the LXC is not running, LXC `ufw` status is inactive. Something is blocking the ports 3000 & 4000, but I couldn't figure out what....Can anyone help?

## Solution: Buying xandsol and pNode
**@Zedok:** Just a heads up to disable your DM. If no help is provided here, open-a-ticket
**@Elaine:** Hi can someone help me to buy some xandsol and then help to buy and run a pnode.
**@Zedok:** Head towards: https://xandsol.xandeum.network/ where you will stake your SOL and get xandsol in return. 
You can buy a p-node here: https://pnodestore.xandeum.network/
As far as help to run a node, read the instructions here: https://pnodes.xandeum.network/
All these links are in the #official-links channel.