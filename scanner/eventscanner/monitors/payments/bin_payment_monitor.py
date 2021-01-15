from scanner.eventscanner.queue.pika_handler import send_to_backend
from scanner.scanner.events.block_event import BlockEvent
from wish_swap.settings_local import BLOCKCHAINS_BY_NUMBER, BLOCKCHAINS


class BinPaymentMonitor:
    network_types = ['Binance-Chain']
    event_type = 'payment'
    queue = 'Binance-Chain'
    allowed = BLOCKCHAINS['Binance-Chain']['token']['address']
    assets = BLOCKCHAINS['Binance-Chain']['token']['symbol']

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_types:
            return
        for key in block_event.transactions_by_address.keys():
            for transaction in block_event.transactions_by_address[key]:
                address = transaction.outputs[0].address
                if address not in cls.allowed or transaction.outputs[0].index not in cls.assets:
                    print('Wrong address or token. Skip Transaction')
                    continue

                amount = transaction.outputs[0].value

                message = {
                    'address': transaction.inputs,
                    'transactionHash': transaction.tx_hash,
                    'amount': int(str(amount).replace('.', '')),
                    'memo': transaction.outputs[0].raw_output_script[1:],
                    'status': 'COMMITTED',
                    'blockchain': BLOCKCHAINS_BY_NUMBER[int(transaction.outputs[0].raw_output_script[0])]
                }

                send_to_backend(cls.event_type, cls.queue, message)