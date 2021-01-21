from pubsub import pub

from scanner.eventscanner.monitors.payments import (BinPaymentMonitor, EthPaymentMonitor, BSPaymentMonitor)
from scanner.eventscanner.monitors import transfer

pub.subscribe(BinPaymentMonitor.on_new_block_event, 'Binance-Chain')
pub.subscribe(EthPaymentMonitor.on_new_block_event, 'Ethereum')
pub.subscribe(BSPaymentMonitor.on_new_block_event, 'Binance-Smart-Chain')

pub.subscribe(transfer.TransferMonitor.on_new_block_event, 'Ethereum')
pub.subscribe(transfer.BSCTransferMonitor.on_new_block_event, 'Binance-Smart-Chain')