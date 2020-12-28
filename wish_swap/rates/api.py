from wish_swap.settings import BLOCKCHAINS, BINANCE_TRANSFER_FEE, TOKEN_DECIMALS, BLOCKCHAIN_DECIMALS
from web3 import Web3, HTTPProvider
from wish_swap.rates.models import UsdRate


def calculate_commission_in_wish(blockchain, address, amount):
    rate_obj = UsdRate.objects.first()
    if not rate_obj:
        raise Exception('You should run rates_checker.py at least once')

    wish_price = getattr(rate_obj, 'WISH')
    blockchain_info = BLOCKCHAINS[blockchain]

    if blockchain in ('Ethereum', 'Binance-Smart-Chain'):
        w3 = Web3(HTTPProvider(blockchain_info['node']))
        token = blockchain_info['token']
        contract = w3.eth.contract(address=token['address'], abi=token['abi'])
        function = contract.functions.mintToUser(Web3.toChecksumAddress(address), amount)
        gas_limit = function.estimateGas({'from': blockchain_info['address']})
        tx_crypto_price = gas_limit * w3.eth.gasPrice / BLOCKCHAIN_DECIMALS
        usd_rate = getattr(rate_obj, blockchain_info['symbol'])
        tx_usd_price = tx_crypto_price * usd_rate
        tx_wish_price = tx_usd_price / wish_price
        return int(tx_wish_price * TOKEN_DECIMALS)
    elif blockchain == 'Binance-Chain':
        usd_rate = getattr(rate_obj, blockchain_info['symbol'])
        tx_usd_price = BINANCE_TRANSFER_FEE * usd_rate
        tx_wish_price = tx_usd_price / wish_price
        return int(tx_wish_price * TOKEN_DECIMALS)
