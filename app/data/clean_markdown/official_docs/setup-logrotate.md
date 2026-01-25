---
original_filename: devnet.xandeum.network_setup-logrotate_a79a0294.txt
source: https://devnet.xandeum.network/setup-logrotate
ingested_at: 2026-01-20
---

## Setup LogRotate
LogRotate will break your log into a new file daily and keep 7 days of logs and discard old logs.

> Important: Make sure your validator start script starts with exec or your validator will go offline for a time each time the logs rotate.

## Configuration
Run as root user, use `sudo -i`. Copy the following code block and paste into terminal:
```bash
cat > logrotate.agave <<EOF
/home/sol/validator.log {
  rotate 7
  daily
  missingok
  postrotate
    systemctl kill -s USR1 validator.service
  endscript
}
EOF
```
Then, copy the configuration file to the logrotate directory:
```bash
sudo cp logrotate.agave /etc/logrotate.d/agave
```

## Restart Logrotate Service
Restart the logrotate service using the following command:
```bash
sudo systemctl restart logrotate.service
```