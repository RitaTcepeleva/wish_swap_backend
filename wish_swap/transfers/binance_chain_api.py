from subprocess import Popen, PIPE
import json
from wish_swap.settings import NETWORKS


class BinanceChainInterface:
    network = NETWORKS['Binance-Chain']

    def multi_send(self, key, password, symbol, transfers):
        command_list = [
            self.network['cli'], 'send',
            '--from', key,
            '--chain-id', self.network['chain-id'],
            '--node', self.network['node'],
            '--transfers'
        ]
        transfers_info = self._generate_transfers_info(transfers, symbol)
        command_list.extend([transfers_info, '--json'])
        is_ok, data = self._execute_bnbcli_command(command_list, password)
        if not is_ok:
            return is_ok, data
        return is_ok, data['TxHash']

    @staticmethod
    def _generate_transfers_info(transfers, symbol):
        result = '"['
        for address, amount in transfers.items():
            result += '{\"to\":\"' + address + '\",\"amount\":\"' + f'{amount}:{symbol}' + '\"},'
        result = result[:-1] + ']"'
        return result

    @staticmethod
    def _execute_bnbcli_command(command_list, password):
        process = Popen(command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate(input=(password + '\n').encode())
        is_ok = process.returncode == 0
        if is_ok:
            return_data = json.loads(stdout.decode())
        else:
            return_data = stderr.decode()
        return is_ok, return_data
