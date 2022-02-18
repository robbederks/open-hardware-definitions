# Open Hardware Definition Ghidra Loader

Since Ghidra only supports running Java and Python 2 (Jython), we are using [ghidra_bridge](https://github.com/justfoxing/ghidra_bridge) to communicate with these (Python 3) scripts.

## Installation
```
pip install ghidra_bridge
python -m ghidra_bridge.install_server ~/ghidra_scripts
```

You can of course install it in another directory, as long as it's in a folder Ghidra searches for scripts.

## Usage
1. On the Ghidra side, run the `ghidra_bridge_server.py` script. This launches the server which this loader can use for interacting with Ghidra.
2. Run `./ohd_loader.py <DEFINITION NAME or PATH>`
3. Enjoy (and look at the errors and submit PRs to fix those)!