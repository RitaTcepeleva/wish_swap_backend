from wish_swap.payments.models import Payment
from wish_swap.transfers.models import Transfer
from wish_swap.transfers.api import eth_like_token_mint, binance_transfer
from wish_swap.settings import BLOCKCHAINS
from wish_swap.rates.api import calculate_commission_in_wish
from wish_swap.rates.models import WishCommission


def save_payment(tx_hash, address, currency, amount):
    payment = Payment(
        address=address,
        tx_hash=tx_hash,
        currency=currency,
        amount=amount,
    )
    payment.save()
    return payment


def create_transfer(payment, address, currency, amount):
    transfer = Transfer(
        payment=payment,
        address=address,
        currency=currency,
        amount=amount,
    )
    transfer.save()
    return transfer


def parse_payment(message):
    tx_hash = message['transactionHash']
    from_blockchain = message['fromBlockchain']
    to_blockchain = message['blockchain']
    from_address = message['address']
    to_address = message['memo']
    amount = message['amount']
    from_currency = BLOCKCHAINS[from_blockchain]['token']['symbol']
    to_currency = BLOCKCHAINS[to_blockchain]['token']['symbol']
    if not Payment.objects.filter(tx_hash=tx_hash, currency=from_currency).count() > 0:
        payment = save_payment(tx_hash, from_address, from_currency, amount)
        commission = calculate_commission_in_wish(to_blockchain, to_address, amount)
        transfer = create_transfer(payment, to_address, to_currency, amount - commission)

        wish_commission_obj = WishCommission.objects.first() or WishCommission()
        wish_commission_obj.amount += commission
        wish_commission_obj.save()

        if to_blockchain in ('Ethereum', 'Binance-Smart-Chain'):
            try:
                transfer.tx_hash = eth_like_token_mint(
                    blockchain_info=BLOCKCHAINS[to_blockchain],
                    address=transfer.address,
                    amount=transfer.amount,
                )
                transfer.status = 'TRANSFERRED'
            except Exception as e:
                transfer.tx_error = repr(e)
                transfer.status = 'FAIL'
            transfer.save()
        elif to_blockchain == 'Binance-Chain':
            binance_transfer(BLOCKCHAINS[to_blockchain], to_address, amount)
        else:
            print('parsing payment: Unknown blockchain', flush=True)
    else:
        print(f'parsing payment: Tx {tx_hash} already registered', flush=True)
