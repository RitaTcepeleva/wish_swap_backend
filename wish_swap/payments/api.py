from wish_swap.payments.models import Payment
from wish_swap.transfers.models import Transfer
from wish_swap.transfers.api import eth_like_token_mint, binance_transfer
from wish_swap.settings import BLOCKCHAINS, TOKEN_DECIMALS
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
        payment = Payment(address=from_address, tx_hash=tx_hash, currency=from_currency, amount=amount)
        payment.save()
        print(f'parsing payment: Payment {payment.tx_hash} from {payment.address} '
              f'for {payment.amount / TOKEN_DECIMALS} {payment.currency} successfully saved', flush=True)

        commission = calculate_commission_in_wish(to_blockchain, to_address, amount)

        print(f'parsing payment: Transfer commission is {commission / TOKEN_DECIMALS} WISH', flush=True)
        transfer = create_transfer(payment, to_address, to_currency, amount - commission)

        wish_commission_obj = WishCommission.objects.first() or WishCommission()
        wish_commission_obj.amount += commission
        wish_commission_obj.save()
        print('parsing payment: Commission saved', flush=True)
        print(f'parsing payment: Total commission amount is '
              f'{wish_commission_obj.amount / TOKEN_DECIMALS} WISH', flush=True)

        if to_blockchain in ('Ethereum', 'Binance-Smart-Chain'):
            try:
                transfer.tx_hash = eth_like_token_mint(
                    blockchain_info=BLOCKCHAINS[to_blockchain],
                    address=transfer.address,
                    amount=transfer.amount,
                )
                transfer.status = 'TRANSFERRED'
                print(f'parsing payment: Successful transfer {transfer.tx_hash} to {transfer.address} '
                      f'for {transfer.amount / TOKEN_DECIMALS} {transfer.currency}', flush=True)
                transfer.save()
                print('parsing payment: Transfer saved', flush=True)
            except Exception as e:
                transfer.tx_error = repr(e)
                transfer.status = 'FAIL'
                print(f'parsing payment: Transfer failed with exception {transfer.tx_error}', flush=True)
                transfer.save()
                print('parsing payment: Transfer saved', flush=True)
        elif to_blockchain == 'Binance-Chain':
            binance_transfer(BLOCKCHAINS[to_blockchain], to_address, amount)
        else:
            print('parsing payment: Unknown blockchain', flush=True)
    else:
        print(f'parsing payment: Tx {tx_hash} already registered', flush=True)
