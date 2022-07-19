# This a simple tool for Chia offer operations

## How to use this

- You need to install the latest Chia wallet (> 1.4.0)
- Run this with Python 3.7+
- Terminal command: 


    python3 tool.py -h


## Use Cases

- Cancel all pending offers related to a CAT, e.g USDS (-i = CAT Asset ID).


    python3 tool.py cancel -f [your_wallet_fingerprint] -i 6d95dae356e32a71db5ddcb42224754a02524c615c5fc35f568c2af04774e589 -m [TX_FEE_IN_MOJO]

- Cancel all pending offers related to a NFT (-i = NFT Launcher ID).


    python3 tool.py cancel -f [your_wallet_fingerprint] -i 7e3221cf4f4b7b8737d474276cdb996a51b8437ab774e6c222243c338981ff47 -m [TX_FEE_IN_MOJO]

- If you just want a dry run for all pending offers, add --dry_run true. e.g.


    python3 tool.py cancel -f 3284271771 -a true --dry_run true

- Cancel all offers need or require XCH


    python3 tool.py cancel -f [your_wallet_fingerprint] -m [TX_FEE_IN_MOJO]