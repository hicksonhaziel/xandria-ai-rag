---
original_filename: xandeum_web3_js_docs3.txt
source: https://github.com/Xandeum/xandeum-web3.js
ingested_at: 2026-01-20
---

# Xandeum Web3 Library v1.12.0
## Overview
The Xandeum Web3 Library provides a set of functions for interacting with the Solana blockchain.

## Functions
### peek
> **peek**(`fsid`, `path`, `startPosition`, `endPosition`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to perform a "peek" operation on a file within a file system.
#### Parameters
* `fsid`: `string` - A stringified integer representing the file system ID in which the file resides.
* `path`: `string` - The path to the file to be peeked.
* `startPosition`: `number` - The starting byte offset (inclusive) to begin reading from.
* `endPosition`: `number` - The ending byte offset (exclusive) to stop reading at.
* `wallet`: `PublicKey` - The public key of the wallet that will sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the peek instruction.

### poke
> **poke**(`fsid`, `path`, `position`, `wallet`, `dataKey`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to perform a poke operation, which writes data to a file at the specified path and byte position.
#### Parameters
* `fsid`: `string` - A stringified integer representing the file system ID where the file resides.
* `path`: `string` - The path to the file to be written to.
* `position`: `number` - The byte offset in the file where data should be written.
* `wallet`: `PublicKey` - The public key of the wallet that signs and authorizes the transaction.
* `dataKey`: `PublicKey` - A public key of a data account that holds the content to be written to the file.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the poke instruction.

### removeDirectory
> **removeDirectory**(`fsid`, `path`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to perform a "remove directory" operation in a file system, identified by a file system ID (`fsid`).
#### Parameters
* `fsid`: `string` - A stringified integer representing the file system ID containing the directory.
* `path`: `string` - The full path to the directory that should be removed.
* `wallet`: `PublicKey` - The public key of the wallet that will sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the remove directory instruction.

### removeFile
> **removeFile**(`fsid`, `path`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to remove a file from a file system, identified by a file system ID (`fsid`) and a UTF-8 encoded file path.
#### Parameters
* `fsid`: `string` - A stringified integer representing the file system ID in which the file resides.
* `path`: `string` - The full path to the file to be deleted.
* `wallet`: `PublicKey` - The public key of the wallet that signs and authorizes the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the remove file instruction.

### renamePath
> **renamePath**(`fsid`, `oldPath`, `name`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to rename (or move) a file or directory within a file system, based on a provided file system ID (`fsid`).
#### Parameters
* `fsid`: `string` - A stringified integer representing the file system ID where the path exists.
* `oldPath`: `string` - The current path of the file or directory to be renamed or moved.
* `name`: `string` - The new name to assign to the file or directory.
* `wallet`: `PublicKey` - The public key of the wallet that signs and authorizes the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the rename path instruction.

### subscribeResult
> **subscribeResult**(`connection`, `tx`, `onResult`, `onError?`, `onClose?`): `void`
Opens a WebSocket connection and subscribes to the result of a transaction via the custom `xandeumResultSubscribe` method.
#### Parameters
* `connection`: `Connection` - The solana web3 connection with Xandeum-compatible JSON-RPC endpoint (e.g., `'https://api.devnet.solana.com'`).
* `tx`: `string` - The transaction ID you want to listen for results from.
* `onResult`: (`value`) => `void` - Callback to handle incoming result messages. Triggered when a valid response is received.
* `onError?`: (`err`) => `void` - (Optional) Callback triggered if a WebSocket error occurs.
* `onClose?`: () => `void` - (Optional) Callback triggered when the WebSocket connection closes.

### unsubscribeResult
> **unsubscribeResult**(`connection`, `subscriptionId`): `void`
Sends a WebSocket JSON-RPC message to unsubscribe from a previously subscribed transaction result using the `xandeumResultUnsubscribed` method (note: custom method, ensure server-side implementation matches).
#### Parameters
* `connection`: `Connection` - The solana web3 connection with Xandeum-compatible JSON-RPC endpoint (e.g., `'https://api.devnet.solana.com'`).
* `subscriptionId`: `string` - The ID of the active subscription you want to cancel.