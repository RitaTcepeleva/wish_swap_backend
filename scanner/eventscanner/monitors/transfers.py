from scanner.eventscanner.queue.pika_handler import send_to_backend
from scanner.mywish_models.models import Transfer, session
from scanner.scanner.events.block_event import BlockEvent

class TransferMonitor:
    network_type=['Ethereum']
    queue='Ethereum'
    event_type = 'transfer'

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_type:
            return

        tx_hashes = set()
        for address_transactions in block_event.transactions_by_address.values():
            for transaction in address_transactions:
                tx_hashes.add(transaction.tx_hash)

        transfers = session \
            .query(Transfer) \
            .filter(Transfer.tx_hash.in_(tx_hashes))\
            .distinct(Transfer.tx_hash) \
            .all()



        for transfer in transfers:
            try:
                tx_receipt = block_event.network.get_tx_receipt(transfer.tx_hash)
                success = tx_receipt.success
            except:
                print('Error on getting tx_receipt, skip')
                success = True

            message = {
                'transactionHash': transfer.tx_hash,
                'transferId': transfer.id,
                'amount': int(transfer.amount),
                'success': success,
                'status': 'COMMITTED',
            }
            send_to_backend(cls.event_type, cls.queue, message)


class BSCTransferMonitor(TransferMonitor):
    network_type = ['Binance-Smart-Chain']
    queue='Binance-Smart-Chain'
