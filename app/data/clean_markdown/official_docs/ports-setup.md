---
original_filename: devnet.xandeum.network_ports-setup_7320378f.txt
source: https://devnet.xandeum.network/ports-setup
ingested_at: 2026-01-20
---

## Ports Setup
The `~/validator-start.sh` script assumes ports 8000-10000 tcp & udp are internally forwarded to the validator via a DST NAT (port forwarding) Rule.

To set up port forwarding, please run a few searches on the following terms:
* how to port forward my router
* setup virtual server on my router
* how to set destination nat rules on my firewall

The overall idea is that when a request is made to your Public IP Address on a port (ie 8000) Your router has to take that request and forward it through your router (firewall) and submit it to the Internal IP address of your validator.

> It would be beneficial to the entire cluster if your public IP address from your internet provider is set as static. This means that you will always have the same IP address even if you reboot your modem/router or if you change your equipment.

> It would also be beneficial if you are running your validator behind a router (ie running at home or office vs data center) to make sure you set up your validator server to always acquire the same IP address from your router. This can be done during the installation of ubuntu or it can be done in your router by way of a function called a dhcp reservation.

## Configuration Recommendations
To achieve a stable setup, consider the following:
* Set up a static public IP address
* Set up a static private IP address using dhcp reservation or during ubuntu installation

## Additional Information
For more information on port forwarding and setting up a static IP address, please refer to your router's documentation and the search terms provided above.