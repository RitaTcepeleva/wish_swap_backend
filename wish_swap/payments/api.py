from wish_swap.payments.models import Payment
from wish_swap.settings import NETWORKS_BY_NUMBER, NETWORKS
from wish_swap.tokens.models import Token
from wish_swap.transfers.models import Transfer
from web3 import Web3, HTTPProvider


def check_gas_price(network_name):
    if network_name not in ('Ethereum', 'Binance-Smart-Chain'):
        return True
    network = NETWORKS[network_name]
    w3 = Web3(HTTPProvider(network['node']))
    return w3.eth.gasPrice <= network['gas_price_max']


def parse_payment(message):
    network_number = message['networkNumber']
    try:
        to_network = NETWORKS_BY_NUMBER[network_number]
    except KeyError:
        print(f'PARSING PAYMENT: network associated with number {network_number} doesn`t exist!', flush=True)
        return

    tx_hash = message['transactionHash']
    from_address = message['address']
    to_address = message['toAddress']
    amount = message['amount']
    from_token = Token.objects.get(pk=message['tokenId'])

    if not Payment.objects.filter(tx_hash=tx_hash, token=from_token).count() > 0:
        payment = Payment(address=from_address, tx_hash=tx_hash, token=from_token, amount=amount)
        payment.save()
        print(f'PARSING PAYMENT: payment {payment.tx_hash} from {payment.address} '
              f'for {amount / (10 ** from_token.decimals)} {from_token.symbol} successfully saved', flush=True)

        try:
            to_token = from_token.dex[to_network]
        except Token.DoesNotExist:
            print(f'PARSING PAYMENT: matching token doesn`t exist in {to_network} network!', flush=True)
            return

        fee_amount = to_token.fee * (10 ** to_token.decimals)

        transfer = Transfer(
            payment=payment,
            token=to_token,
            address=to_address,
            amount=amount - fee_amount,
            fee_address=to_token.fee_address,
            fee_amount=fee_amount,
        )
        transfer.save()

        if not check_gas_price(to_network):
            transfer.status = 'HIGH GAS PRICE'
            transfer.save()
            print(f'PARSING PAYMENT: {transfer.token.symbol} transfer will be executed later '
                  f'due to high gas price in {to_network} network', flush=True)
            return

        transfer.execute()
        transfer.save()

        if transfer.status == 'FAIL':
            print(f'PARSING PAYMENT: transfer failed with error {transfer.tx_error}', flush=True)
        else:
            decimals = (10 ** transfer.token.decimals)
            symbol = transfer.token.symbol
            print(f'PARSING PAYMENT: successful transfer {transfer.tx_hash} '
                  f'{transfer.amount / decimals} {symbol} to {transfer.address}, '
                  f'(fee) {transfer.fee_amount / decimals} {symbol} to {transfer.fee_address}', flush=True)

    else:
        print(f'PARSING PAYMENT: tx {tx_hash} already registered', flush=True)
