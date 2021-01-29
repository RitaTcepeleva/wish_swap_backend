from wish_swap.transfers.models import Transfer
from celery import shared_task
from wish_swap.transfers.api import send_transfer_to_queue


@shared_task
def push_transfers():
    transfers = Transfer.objects.filter(status='HIGH GAS PRICE')
    if not transfers.count():
        print(f'PUSHING TRANSFERS: no transfers to push', flush=True)
        return
    print(f'PUSHING TRANSFERS: start pushing...', flush=True)
    for transfer in transfers:
        send_transfer_to_queue(transfer)
    print(f'PUSHING TRANSFERS: pushing completed', flush=True)
