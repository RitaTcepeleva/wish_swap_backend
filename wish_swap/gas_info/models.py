from django.db import models
from web3 import Web3, HTTPProvider
from wish_swap.settings_local import NETWORKS


class GasInfo(models.Model):
    network = models.CharField(max_length=100, primary_key=True)
    price_limit = models.IntegerField()

    @property
    def price(self):
        network = NETWORKS[self.network]
        w3 = Web3(HTTPProvider(network['node']))
        return int(w3.eth.gasPrice / (10 ** 9))
