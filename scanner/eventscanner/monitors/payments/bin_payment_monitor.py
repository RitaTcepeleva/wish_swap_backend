from scanner.eventscanner.queue.pika_handler import send_to_backend
from scanner.mywish_models.models import Dex, Token, SwapAddress, session
from scanner.scanner.events.block_event import BlockEvent


class BinPaymentMonitor:
    network_types = ['Binance-Chain']
    event_type = 'payment'
    queue = 'Binance-Chain'

    @classmethod
    def network(cls, model):
        s = 'network'
        return getattr(model, s)


    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_types:
            return
        tokens = session.query(Token).filter(cls.network(Token).in_(cls.network_types)).all()
        for key in block_event.transactions_by_address.keys():
            for transaction in block_event.transactions_by_address[key]:
                address = transaction.outputs[0].address
                from_address = transaction.inputs
                for token in tokens:
                    id=[token.swap_address_id]
                    swap_address = session.query(SwapAddress).filter(getattr(SwapAddress, 'id').in_(id)).first()
                    print(from_address.lower(), swap_address.address.lower())
                    if from_address.lower()==swap_address.address.lower():
                        print('Outcoming transaction. Skip Transaction')
                        continue
                    if address not in swap_address.address or transaction.outputs[0].index not in token.symbol:
                        print('Wrong address or token. Skip Transaction')
                        continue

                    amount = transaction.outputs[0].value

                    message = {
                        'tokenId': token.id,
                        'address': transaction.inputs,
                        'transactionHash': transaction.tx_hash,
                        'amount': int(str(amount).replace('.', '')),
                        'toAddress': transaction.outputs[0].raw_output_script[1:],
                        'status': 'COMMITTED',
                        'networkNumber': int(transaction.outputs[0].raw_output_script[0])
                    }

                    send_to_backend(cls.event_type, cls.queue, message)