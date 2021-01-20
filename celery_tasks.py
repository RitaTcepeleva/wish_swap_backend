from wish_swap.transfers.models import Transfer
from wish_swap.payments.api import check_gas_price
from celery import shared_task


@shared_task
def push_transfers():
    transfers = Transfer.objects.filter(status='HIGH GAS PRICE')
    for transfer in transfers:
        if not check_gas_price(transfer.token.network):
            print('PUSHING TRANSFERS: aborting pushing due to high gas price', flush=True)
            return

        transfer.execute()
        transfer.save()

        if transfer.status == 'FAIL':
            print(f'PUSHING TRANSFERS: transfer failed with error {transfer.tx_error}', flush=True)
            print('PUSHING TRANSFERS: aborting pushing', flush=True)
        else:
            decimals = (10 ** transfer.token.decimals)
            symbol = transfer.token.symbol
            print(f'PUSHING TRANSFERS: successful transfer {transfer.tx_hash} '
                  f'{transfer.amount / decimals} {symbol} to {transfer.address}, '
                  f'(fee) {transfer.fee_amount / decimals} {symbol} to {transfer.fee_address}', flush=True)
    print(f'PUSHING TRANSFERS: pushing completed', flush=True)
