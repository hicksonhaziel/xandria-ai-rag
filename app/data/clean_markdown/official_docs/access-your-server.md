---
original_filename: devnet.xandeum.network_access-your-server_cb07be7b.txt
source: https://devnet.xandeum.network/access-your-server
ingested_at: 2026-01-20
---

## Accessing Your Server
To access your server, you will need the username, password, and IP address provided by your server hosting company. You will use a terminal application to interact with the server via text-based prompts. The default administrator user is usually called `root` and has unlimited power in the operating system. `root` access is required for admin-level commands. A standard non-privileged user will be used for day-to-day tasks.

## Apple/Mac
To access your server using a CLI (command line interface) on a Mac, you can use the built-in Terminal app. 
To access your server in Terminal, you will use the command:
```bash
ssh root@<ipaddress>
```
For more information, see the [What is Terminal on Mac guide](https://).

## Windows
If you use a Windows PC, you will need a terminal application such as PuTTY. You can learn about it on their website: [putty.org](http://putty.org). Download the correct version for your machine, most likely the [64-bit x86: putty-64bit-0.79-installer.msi](http://).
To access your server in PuTTY, enter `root@<ipaddress>` into the Host Name field.