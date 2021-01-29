import time
from wish_swap.transfers.models import Transfer
from wish_swap.networks.models import GasInfo
from celery import shared_task
from wish_swap.settings_local import PUSHING_TRANSFERS_TIMEOUT_SECS
from wish_swap.transfers.api import send_transfer_to_queue


@shared_task
def push_transfers():
    transfers = Transfer.objects.filter(status='HIGH GAS PRICE')
    if not transfers.count():
        print(f'PUSHING TRANSFERS: no transfers to push', flush=True)
        return
    print(f'PUSHING TRANSFERS: start pushing...', flush=True)
    for transfer in transfers:
        network = transfer.token.network
        if network in ('Ethereum', 'Binance-Smart-Chain'):
            gas_info = GasInfo.objects.get(network=network)
            gas_price = gas_info.price
            gas_price_limit = gas_info.price_limit
            if gas_price > gas_price_limit:
                print(f'PUSHING TRANSFERS: {transfer.token.symbol} abort pushing transfers due to high gas '
                      f'price in {network} network ({gas_price} Gwei > {gas_price_limit} Gwei)', flush=True)
                return

        send_transfer_to_queue(transfer)
        time.sleep(PUSHING_TRANSFERS_TIMEOUT_SECS)
    print(f'PUSHING TRANSFERS: pushing completed', flush=True)
