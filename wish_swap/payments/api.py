from wish_swap.payments.models import Payment
from wish_swap.settings import NETWORKS_BY_NUMBER
from wish_swap.tokens.models import Token
from wish_swap.transfers.models import Transfer
from wish_swap.networks.models import GasInfo


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
              f'for {amount / (10 ** from_token.decimals)} {from_token.symbol} successfully saved', flush=True)

        transfer = create_transfer_if_payment_valid(payment)
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
