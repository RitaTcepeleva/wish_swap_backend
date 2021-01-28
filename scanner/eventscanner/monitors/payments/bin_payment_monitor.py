from scanner.eventscanner.queue.pika_handler import send_to_backend
from scanner.mywish_models.models import Dex, Token, session
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
        #get all token instances assigned to binance-chain network
        tokens = session.query(Token).filter(cls.network(Token).in_(cls.network_types)).all()
        for key in block_event.transactions_by_address.keys():
            for transaction in block_event.transactions_by_address[key]:
                address = transaction.outputs[0].address
                from_address = transaction.inputs
                for token in tokens:
                    swap_address = token.swap_address
                    print(from_address.lower(), swap_address.lower())
                    #Check outcoming transactions
                    if from_address.lower()==swap_address.lower():
                        print('Outcoming transaction. Skip Transaction')
                        continue
                    #Check if transaction doesn't belong to current token
                    if address not in swap_address or transaction.outputs[0].index not in token.symbol:
                        print('Wrong address or token. Skip Transaction')
                        continue

                    amount = transaction.outputs[0].value
                    #delete spaces for backend
                    output=transaction.outputs[0].raw_output_script.replace(' ', '')
                    #check memo field (required for bridge to work)
                    if len(output)==0:
                        print('No memo field')
                        toAddress=''
                        networkNumber = -1
                    elif output[0].isalpha():
                        print('first symbol is alpha')
                        networkNumber = -1
                        toAddress = output
                    else:
                        networkNumber = int(output[0])
                        toAddress = output[1:]
                    message = {
                        'tokenId': token.id,
                        'address': transaction.inputs,
                        'transactionHash': transaction.tx_hash,
                        'amount': int(str(amount).replace('.', '')),
                        'toAddress': toAddress,
                        'status': 'COMMITTED',
                        'networkNumber': networkNumber
                    }

                    send_to_backend(cls.event_type, cls.queue, message)