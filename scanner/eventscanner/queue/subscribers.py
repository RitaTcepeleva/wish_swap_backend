from pubsub import pub

from scanner.eventscanner.monitors.payments import (BinPaymentMonitor, EthPaymentMonitor, BSPaymentMonitor)

pub.subscribe(BinPaymentMonitor.on_new_block_event, 'BINANCE_MAINNET')
pub.subscribe(EthPaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')
pub.subscribe(BSPaymentMonitor.on_new_block_event, 'BINANCE_SMART_MAINNET')
