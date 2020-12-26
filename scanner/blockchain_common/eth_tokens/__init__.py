import json
import os

with open(os.path.join(os.getcwd(), 'scanner/blockchain_common/eth_tokens/erc20_abi.json'), 'r') as f:
    erc20_abi = json.load(f)