---
original_filename: Xandeum_Pod_APT_Repository.txt
source: https://github.com/Xandeum/pod-apt-package
ingested_at: 2026-01-20
---

# Xandeum Pod APT Repository
[![source](https://github.com/Xandeum/pod-apt-package)](https://github.com/Xandeum/pod-apt-package)
## Installation Instructions
To install the pod binary on any Debian/Ubuntu-based system:
1. **Enable HTTPS transport**: 
   ```bash
sudo apt-get install -y apt-transport-https ca-certificates
```
2. **Add the Xandeum APT repository**: 
   ```bash
echo "deb [trusted=yes] https://xandeum.github.io/pod-apt-package/ stable main" | sudo tee /etc/apt/sources.list.d/xandeum-pod.list
```
3. **Update package index**: 
   ```bash
sudo apt-get update
```
4. **Install the pod binary**: 
   ```bash
sudo apt-get install pod
```