from scanner.eventscanner.queue.pika_handler import send_to_backend
#from mywish_models.models import ExchangeRequests, session
from scanner.scanner.events.block_event import BlockEvent
from wish_swap.settings_local import BLOCKCHAINS_BY_NUMBER, BLOCKCHAINS


class EthPaymentMonitor:

    network_types = ['Ethereum']
    event_type = 'payment'
    queue = 'Ethereum'
    token = BLOCKCHAINS['Ethereum']['token']
    tokens = [{token['symbol']: token['address']}]

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_types:
            return
        addresses = block_event.transactions_by_address.keys()
        for token_name, token_address in cls.tokens.items():
            token_address = token_address.lower()
            if token_address in addresses:
                transactions = block_event.transactions_by_address[token_address]
                cls.handle(token_address, token_name, transactions, block_event.network)
        
        
    @classmethod
    def handle(cls, token_address: str, token_name, transactions, network):
        for tx in transactions:
            if token_address.lower() != tx.outputs[0].address.lower():
                continue

            processed_receipt = network.get_processed_tx_receipt(tx.tx_hash, token_name)
            if not processed_receipt:
                print('{}: WARNING! Can`t handle tx {}, probably we dont support this event'.format(
                    cls.network_types[0], tx.tx_hash), flush=True)
                return
            print(processed_receipt)
            transfer_from = processed_receipt[0].args.user
            amount = processed_receipt[0].args.amount
            blockchain = BLOCKCHAINS_BY_NUMBER[processed_receipt[0].args.blockchain]
            swap_to = processed_receipt[0].args.newAddress

        
            tx_receipt = network.get_tx_receipt(tx.tx_hash)
            if tx_receipt.success==True:
                success='COMMITTED'
            else:
                success='ERROR'
            print(tx.outputs[0].raw_output_script)
            message = {
                'address': transfer_from,
                'transactionHash': tx.tx_hash,
                'amount': amount,
                'memo': swap_to,
                'status': success,
                'blockchain': blockchain
            }
            
            send_to_backend(cls.event_type, cls.queue, message)


class BSPaymentMonitor(EthPaymentMonitor):
    network_types = ['Binance-Smart-Chain']
    event_type = 'payment'
    queue = 'Binance-Smart-Chain'
    token = BLOCKCHAINS['Binance-Smart-Chain']['token']
    tokens = [{token['symbol']: token['address']}]
