from django.db import models
from web3 import Web3, HTTPProvider
from wish_swap.settings_local import NETWORKS


class GasInfo(models.Model):
    network = models.CharField(max_length=100, primary_key=True)
    price_limit = models.DecimalField(max_digits=100, decimal_places=0)

    @property
    def price(self):
        network = NETWORKS[self.name]
        w3 = Web3(HTTPProvider(network['node']))
        return w3.eth.gasPrice
