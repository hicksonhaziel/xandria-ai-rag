---
original_filename: xandeum_web3_js_docs1.txt
source: https://github.com/Xandeum/xandeum-web3.js
ingested_at: 2026-01-20
---

# Xandeum Web3 Library
## armageddon
### Function: armageddon()
> **armageddon**(`fsid`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction that triggers the "armageddon" instruction on the specified file system (fsid).
#### Parameters
* **fsid**: `string` - A stringified integer representing the file system ID to be used in the instruction.
* **wallet**: `PublicKey` - The public key of the wallet that will sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the armageddon instruction.

## bigbang
### Function: bigbang()
> **bigbang**(`wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction that triggers the "bigbang" instruction and creates a new file system.
#### Parameters
* **wallet**: `PublicKey` - The public key of the wallet that will sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the bigbang instruction.

## copyPath
### Function: copyPath()
> **copyPath**(`fsid`, `srcPath`, `destPath`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to copy a file or directory from one path to another.
#### Parameters
* **fsid**: `string` - The unique numeric identifier representing the target file system.
* **srcPath**: `string` - The source path to copy from (e.g., `/documents/report.txt`).
* **destPath**: `string` - The destination path to copy to (e.g., `/archive/report.txt`).
* **wallet**: `PublicKey` - The wallet public key used to sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the copyPath instruction.
#### Throws
Will throw an error if `srcPath` or `destPath` contains invalid characters.

## createDirectory
### Function: createDirectory()
> **createDirectory**(`fsid`, `path`, `name`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to create a new directory within a file system.
#### Parameters
* **fsid**: `string` - A numeric filesystem identifier used to scope the directory creation.
* **path**: `string` - The parent path where the directory should be created (e.g., `/documents`).
* **name**: `string` - The name of the new directory (e.g., `reports`).
* **wallet**: `PublicKey` - The signer’s public key that authorizes the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the createDirectory instruction.
#### Throws
Will throw an error if `path` or `name` contains invalid characters.

## createFile
### Function: createFile()
> **createFile**(`fsid`, `path`, `name`, `wallet`): `Promise`\<`Transaction`\>
Constructs a Solana transaction to create a new file within a file system, identified by a file system ID (`fsid`).
#### Parameters
* **fsid**: `string` - A stringified integer representing the file system ID where the file is to be created.
* **path**: `string` - The absolute or relative path within the file system where the file should be created.
* **name**: `string` - The name of the new file or directory to be created.
* **wallet**: `PublicKey` - The public key of the wallet that will sign and authorize the transaction.
#### Returns
`Promise`\<`Transaction`\> - A Promise that resolves to a Solana `Transaction` object containing the createFile instruction.
#### Throws
Will throw an error if `path` or `name` contains invalid characters.