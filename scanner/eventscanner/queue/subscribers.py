from pubsub import pub

from scanner.eventscanner.monitors.payments import (BinPaymentMonitor, EthPaymentMonitor, BSPaymentMonitor)
from scanner.eventscanner.monitors import transfers

pub.subscribe(BinPaymentMonitor.on_new_block_event, 'Binance-Chain')
pub.subscribe(EthPaymentMonitor.on_new_block_event, 'Ethereum')
pub.subscribe(BSPaymentMonitor.on_new_block_event, 'Binance-Smart-Chain')

#pub.subscribe(transfers.TransferMonitor.on_new_block_event, 'Ethereum')
#pub.subscribe(transfers.BSCTransferMonitor.on_new_block_event, 'Binance-Smart-Chain')