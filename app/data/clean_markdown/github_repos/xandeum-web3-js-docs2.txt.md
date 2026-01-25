---
original_filename: xandeum_web3_js_docs2.txt
source: https://github.com/Xandeum/xandeum-web3.js
ingested_at: 2026-01-20
---

# Xandeum Web3 Library
## exists
### Function: exists()
> **exists**(`connection`, `path`): `Promise`\<`any`\>
Sends a JSON-RPC request to the Xandeum RPC endpoint to check if a file or directory exists.
#### Parameters
* `connection`: The solana web3 connection with Xandeum-compatible JSON-RPC endpoint (e.g., `'https://api.devnet.solana.com'`).
* `path`: The filesystem path to check (e.g., `/documents/myfile.txt`).
#### Returns
`Promise`\<`any`\>
A `Promise<any>` resolving to the RPC response JSON, typically including a `result` field indicating existence (e.g., `true` or `false`), or `null` if not found.

## getMetadata
### Function: getMetadata()
> **getMetadata**(`connection`, `path`): `Promise`\<`any`\>
Sends a JSON-RPC request to the Xandeum RPC endpoint to retrieve metadata about a file or directory at the given path.
#### Parameters
* `connection`: The solana web3 connection with Xandeum-compatible JSON-RPC endpoint (e.g., `'https://api.devnet.solana.com'`).
* `path`: The filesystem path to query metadata for (e.g., `/documents/myfile.txt`).
#### Returns
`Promise`\<`any`\>
A `Promise<any>` resolving to the parsed JSON response from the RPC server, typically containing a `result` object with metadata fields.

## getXandeumResult
### Function: getXandeumResult()
> **getXandeumResult**(`connection`, `signature`): `Promise`\<`any`\>
Sends a JSON-RPC request to the Xandeum-compatible endpoint to retrieve the result of a transaction previously submitted with a specific signature.
#### Parameters
* `connection`: The Solana web3 connection object pointing to a Xandeum-compatible RPC endpoint.
* `signature`: The transaction signature string whose result should be queried.
#### Returns
`Promise`\<`any`\>
A `Promise<any>` resolving to the parsed JSON response from the RPC server, which includes the result of the transaction if available.

## listDirectoryEntry
### Function: listDirectoryEntry()
> **listDirectoryEntry**(`connection`, `path`): `Promise`\<`any`\>
Sends a JSON-RPC request to the Xandeum RPC endpoint to list all entries (files and subdirectories) within a specified path.
#### Parameters
* `connection`: The solana web3 connection with Xandeum-compatible JSON-RPC endpoint (e.g., `'https://api.devnet.solana.com'`).
* `path`: The filesystem path representing the directory to list (e.g., `/documents`).
#### Returns
`Promise`\<`any`\>
A `Promise<any>` resolving to the parsed JSON response from the RPC server, typically including a `result` array containing directory entry objects.

## move
### Function: move()
> **move**(`fsid`, `srcPath`, `destPath`, `name`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to copy a file or directory from one path to another.
#### Parameters
* `fsid`: The unique numeric identifier representing the target file system.
* `srcPath`: The source path to copy from (e.g., `/documents`).
* `destPath`: The destination path to copy to (e.g., `/archive`).
* `name`: The name of the new file or directory at the destination (e.g., `report.txt`).
* `wallet`: The wallet public key used to sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\>
A Promise that resolves to a Solana `Transaction` object containing the copyPath instruction.
#### Throws
Will throw an error if `srcPath` or `destPath` contains invalid characters.