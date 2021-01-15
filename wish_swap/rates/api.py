from wish_swap.settings import NETWORKS, BINANCE_TRANSFER_FEE, TOKEN_DECIMALS, BLOCKCHAIN_DECIMALS
from web3 import Web3, HTTPProvider
from wish_swap.rates.models import UsdRate


def calculate_wish_fee(network_name, address, amount):
    rate_obj = UsdRate.objects.first()
    if not rate_obj:
        raise Exception('You should run rates_checker.py at least once')

    wish_price = getattr(rate_obj, 'WISH')
    network = NETWORKS[network_name]

    if network_name in ('Ethereum', 'Binance-Smart-Chain'):
        w3 = Web3(HTTPProvider(network['node']))
        token = network['token']
        contract = w3.eth.contract(address=token['address'], abi=token['abi'])
        function = contract.functions.mintToUser(Web3.toChecksumAddress(address), amount)
        gas_limit = function.estimateGas({'from': network['address']})
        tx_crypto_price = gas_limit * w3.eth.gasPrice / BLOCKCHAIN_DECIMALS
        usd_rate = getattr(rate_obj, network['symbol'])
        tx_usd_price = tx_crypto_price * usd_rate
        tx_wish_price = tx_usd_price / wish_price
        return int(tx_wish_price * TOKEN_DECIMALS)
    elif network_name == 'Binance-Chain':
        usd_rate = getattr(rate_obj, network['symbol'])
        tx_usd_price = BINANCE_TRANSFER_FEE * usd_rate
        tx_wish_price = tx_usd_price / wish_price
        return int(tx_wish_price * TOKEN_DECIMALS)
