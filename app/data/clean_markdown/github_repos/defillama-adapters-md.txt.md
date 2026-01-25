---
original_filename: Defillama_Adapters_md.txt
source: https://github.com/Xandeum/DefiLlama-Adapters
ingested_at: 2026-01-20
---

# Defillama Adapters
Follow this guide to create an adapter and submit a PR with it.

## Introduction
To add a volume adapter, submit a PR [here](https://github.com/Xandeum/DefiLlama-Adapters). For liquidations adapters, refer to this README document.

## Guidelines
* Enable "Allow edits by maintainers" when submitting a PR.
* TVL must be computed from blockchain data (see [DefiLlama#432](https://github.com/DefiLlama/DefiLlama-Adapters/issues/432)).
* For assistance, join our Discord.
* To update listing info, edit [this file](https://github.com/DefiLlama/defillama-server/blob/master/defi/src/protocols/data2.ts) and submit a PR.
* Do not edit/push `package-lock.json` file as part of your changes.

## Getting Listed
When creating a PR, please answer questions in [this template](https://github.com/DefiLlama/DefiLlama-Adapters/blob/main/pull_request_template.md).

## Work in Progress
DefiLlama aims to be transparent, accurate, and open source. Suggestions and contributions are welcome on our Discord.

## Testing Adapters
To test adapters, run:
```bash
node test.js projects/pangolin/index.js
```
To run an adapter at a historical timestamp:
```bash
node test.js projects/aave/v3.js 1729080692
```

## Changing RPC Providers
To change RPC providers, create an `.env` file with the following env variables:
```makefile
ETHEREUM_RPC="..."
BSC_RPC="..."
POLYGON_RPC="..."
```
The name of each RPC is `{CHAIN-NAME}_RPC`. Chain names can be found [here](https://github.com/Xandeum/DefiLlama-Adapters).

## Adapter Rules
* Never add extra npm packages. If a chain-level package is needed, ask for consideration.
* Project-specific npm packages will not be accepted.