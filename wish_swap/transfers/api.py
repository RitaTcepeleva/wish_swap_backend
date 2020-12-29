from web3 import Web3, HTTPProvider
from wish_swap.settings import GAS_LIMIT, BNBCLI_PATH
from subprocess import Popen, PIPE
import json


def eth_like_token_mint(blockchain_info, address, amount):
    w3 = Web3(HTTPProvider(blockchain_info['node']))
    tx_params = {
        'nonce': w3.eth.getTransactionCount(blockchain_info['address'], 'pending'),
        'gasPrice': w3.eth.gasPrice,
        'gas': GAS_LIMIT,
    }
    token = blockchain_info['token']
    contract = w3.eth.contract(address=token['address'], abi=token['abi'])
    initial_tx = contract.functions.mintToUser(Web3.toChecksumAddress(address), amount).buildTransaction(tx_params)
    signed_tx = w3.eth.account.signTransaction(initial_tx, blockchain_info['private'])
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hex = tx_hash.hex()
    return tx_hex


def binance_transfer(blockchain, address, amount):
    command_list = ['tbnbcli', 'send',
                    '--from', blockchain['key'],
                    '--to', address,
                    '--amount', f'{amount}:{blockchain["token"]["symbol"]}',
                    '--chain-id', blockchain['chain-id'],
                    '--node', blockchain['node'],
                    '--json']

    process = Popen(command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(input=(blockchain['key-password'] + '\n').encode())
    is_ok = process.returncode == 0
    if is_ok:
        message = json.loads(stdout.decode())
        data = message['TxHash']
    else:
        data = stderr.decode()
    return is_ok, data
