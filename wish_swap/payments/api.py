from wish_swap.payments.models import Payment
from wish_swap.settings import NETWORKS_BY_NUMBER
from wish_swap.tokens.models import Token, Dex
from wish_swap.transfers.models import Transfer
from wish_swap.networks.models import GasInfo
from web3 import Web3, HTTPProvider
from wish_swap.settings import NETWORKS
import requests
import json
from wish_swap.transfers.api import send_transfer_to_queue


def create_transfer_if_payment_valid(payment):
    try:
        to_network = NETWORKS_BY_NUMBER[payment.transfer_network_number]
    except KeyError:
        payment.validation_status = 'INVALID NETWORK NUMBER'
        payment.save()
        print('PARSING PAYMENT: network associated with number '
              f'{payment.transfer_network_number} doesn`t exist!', flush=True)
        return None

    try:
        to_token = payment.token.dex[to_network]
    except Token.DoesNotExist:
        payment.validation_status = 'INVALID NETWORK NUMBER'
        payment.save()
        print(f'PARSING PAYMENT: matching token doesn`t exist in {to_network} network!', flush=True)
        return None

    fee_amount = to_token.fee * (10 ** to_token.decimals)

    if payment.amount - fee_amount <= 0:
        payment.validation_status = 'SMALL AMOUNT'
        payment.save()
        print(f'PARSING PAYMENT: abort transfer due to commission is more than transfer amount', flush=True)
        return None

    payment.validation_status = 'SUCCESS'
    payment.save()

    transfer = Transfer(
        payment=payment,
        token=to_token,
        address=payment.transfer_address,
        amount=payment.amount - fee_amount,
        fee_address=to_token.fee_address,
        fee_amount=fee_amount,
        network=to_token.network,
    )
    transfer.save()
    return transfer


def parse_payment(message):
    network_number = message['networkNumber']
    tx_hash = message['transactionHash']
    from_address = message['address']
    to_address = message['toAddress']
    amount = message['amount']
    from_token = Token.objects.get(pk=message['tokenId'])

    if not Payment.objects.filter(tx_hash=tx_hash, token=from_token).count() > 0:
        payment = Payment(
            token=from_token,
            address=from_address,
            tx_hash=tx_hash,
            amount=amount,
            transfer_address=to_address,
            transfer_network_number=network_number,
        )
        payment.save()
        print(f'PARSING PAYMENT: payment {payment.tx_hash} from {payment.address} '
              f'for {amount / (10 ** from_token.decimals)} {from_token.symbol} to {payment.transfer_address}'
              f' in network {payment.transfer_network_number} successfully saved', flush=True)

        transfer = create_transfer_if_payment_valid(payment)
        if not transfer:
            return

        to_network = transfer.network

        if to_network in ('Ethereum', 'Binance-Smart-Chain'):
            gas_info = GasInfo.objects.get(network=to_network)
            gas_price = gas_info.price
            gas_price_limit = gas_info.price_limit
            if gas_price > gas_price_limit:
                transfer.status = 'HIGH GAS PRICE'
                transfer.save()
                print(f'PARSING PAYMENT: {transfer.token.symbol} transfer will be executed later due to '
                      f'high gas price in {to_network} network ({gas_price} Gwei > {gas_price_limit} Gwei)', flush=True)
                return

        send_transfer_to_queue(transfer)

    else:
        print(f'PARSING PAYMENT: tx {tx_hash} already registered', flush=True)


def parse_payment_manually(tx_hash, network_name, dex_name):
    dex = Dex.objects.get(name=dex_name)
    token = dex[network_name]
    if network_name in ('Ethereum', 'Binance-Smart-Chain'):
        w3 = Web3(HTTPProvider(NETWORKS[token.network]['node']))
        contract = w3.eth.contract(address=token.swap_address, abi=token.swap_abi)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        receipt = contract.events.TransferToOtherBlockchain().processReceipt(tx_receipt)
        if not receipt:
            # TODO: logging
            return

        event = receipt[0].args
        message = {
            'tokenId': token.id,
            'address': event.user,
            'transactionHash': tx_hash,
            'amount': event.amount,
            'toAddress': event.newAddress,
            'networkNumber': event.blockchain
        }
        parse_payment(message)
    elif network_name == 'Binance-Chain':
        url = f'{NETWORKS[network_name]["api-url"]}tx/{tx_hash}?format=json'
        response = requests.get(url)
        json_data = json.loads(response.text)
        data = json_data['tx']['value']['msg'][0]['value']
        memo = json_data['tx']['value']['memo'].replace(' ', '')
        to_address = data['outputs'][0]['address']
        from_address = data['inputs'][0]['address']
        symbol = data['inputs'][0]['coins'][0]['denom']
        amount = data['inputs'][0]['coins'][0]['amount']

        if from_address == token.swap_address:
            # TODO: logging
            return

        if to_address != token.swap_address:
            # TODO: logging
            return

        if symbol != token.symbol:
            # TODO: logging
            return

        message = {
            'tokenId': token.id,
            'address': from_address,
            'transactionHash': tx_hash,
            'amount': int(amount),
            'toAddress': memo[1:],
            'networkNumber': int(memo[0])
        }
        parse_payment(message)
