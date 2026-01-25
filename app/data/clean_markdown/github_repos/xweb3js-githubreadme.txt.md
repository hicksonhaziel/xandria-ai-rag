---
original_filename: xweb3js_githubreadme.txt
source: https://github.com/Xandeum/Xweb3.js
ingested_at: 2026-01-20
---

# Solana JavaScript SDK
Use this to interact with accounts and programs on the Solana network through the Solana JSON RPC API.
source=https://github.com/Xandeum/Xweb3.js

## Installation
For use in Node.js or a web application
```bash
$ npm install --save @solana/web3.js
```
For use in a browser, without a build system
```html
<!-- Development (un-minified) -->
<script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.js"></script>

<!-- Production (minified) -->
<script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.min.js"></script>
```

## Documentation and examples
The Solana Cookbook has extensive task-based documentation using this library.
For more detail on individual functions, see the latest API Documentation

## Getting help
Have a question or a problem? Check the Solana Stack Exchange to see if anyone else is having the same one. If not, post a new question.
Include:
* A detailed description of what you're trying to achieve
* Source code, if possible
* The text of any errors you encountered, with stacktraces if available

## Compatibility
This library requires a JavaScript runtime that supports BigInt and the exponentiation operator. Both are supported in the following runtimes:
### Browsers, by release date:
* Chrome: May 2018
* Firefox: July 2019
* Safari: September 2020
* Mobile Safari: September 2020
* Edge: January 2020
* Opera: June 2018
* Samsung Internet: April 2019
### Runtimes, by version:
* Deno: >=1.0
* Node: >=10.4.0
* React Native: >=0.7.0 using the Hermes engine

## Development environment setup
## Testing
### Unit tests
To run the full suite of unit tests, execute the following in the root:
```bash
$ npm test
```
### Integration tests
Integration tests require a validator client running on your machine.
To install a test validator:
```bash
$ npm run test:live-with-test-validator:setup
```
To start the test validator and run all of the integration tests in live mode:
```bash
$ cd packages/library-legacy
$ npm run test:live-with-test-validator
```

## Speed up build times with remote caching
Cache build artifacts remotely so that you, others, and the CI server can take advantage of each others' build efforts.
Log the Turborepo CLI into the Solana Vercel account
```bash
pnpm turbo login
```
Link the repository to the remote cache
```bash
pnpm turbo link
```

## Contributing
If you found a bug or would like to request a feature, please file an issue. If, based on the discussion on an issue you would like to offer a code change, please make a pull request.

## Disclaimer
All claims, content, designs, algorithms, estimates, roadmaps, specifications, and performance measurements described in this project are done with the Solana Foundation's ("SF") best efforts. It is up to the reader to check and validate their accuracy and truthfulness. Furthermore nothing in this project constitutes a solicitation for investment.

Any content produced by SF or developer resources that SF provides, are for educational and inspiration purposes only. SF does not encourage, induce or sanction the deployment, integration or use of any such applications (including the code comprising the Solana blockchain protocol) in violation of applicable laws or regulations and hereby prohibits any such deployment, integration or use. This includes use of any such applications by the reader (a) in violation of export control or sanctions laws of the United States or any other applicable jurisdiction, (b) if the reader is located in or ordinarily resident in a country or territory subject to comprehensive sanctions administered by the U.S. Office of Foreign Assets Control (OFAC), or (c) if the reader is or is working on behalf of a Specially Designated National (SDN) or a person subject to similar blocking or denied party prohibitions.

The reader should be aware that U.S. export control and sanctions laws prohibit U.S. persons (and other persons that are subject to such laws) from transacting with persons in certain countries and territories or that are on the SDN list. As a project based primarily on open-source software, it is possible that such sanctioned persons may nevertheless bypass prohibitions, obtain the code comprising the Solana blockchain protocol (or other project code or applications) and deploy, integrate, or otherwise use it. Accordingly, there is a risk to individuals that other persons using the Solana blockchain protocol may be sanctioned persons and that transactions with such persons would be a violation of U.S. export controls and sanctions law. This risk applies to individuals, organizations, and other ecosystem participants that deploy, integrate, or use the Solana blockchain protocol code directly (e.g., as a node operator), and individuals that transact on the Solana blockchain through light clients, third party interfaces, and/or wallet software. 

## License
MIT license