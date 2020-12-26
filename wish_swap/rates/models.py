from django.db import models
from wish_swap.settings import COINMARKETCAP_API_URL, COINMARKETCAP_API_KEY
import json
import requests


class WishCommission(models.Model):
    amount = models.DecimalField(max_digits=100, decimal_places=0, default=0)


class UsdRate(models.Model):
    ETH = models.FloatField()
    BNB = models.FloatField()
    WISH = models.FloatField()
    datetime = models.DateTimeField(auto_now=True)

    def update(self):
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        }
        params = {'symbol': 'WISH,ETH,BNB'}

        response = requests.get(url=COINMARKETCAP_API_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception('Cannot update rates')
        response_data = json.loads(response.text)['data']

        for currency, data in response_data.items():
            usd_rate = data['quote']['USD']['price']
            setattr(self, currency, usd_rate)
        self.save()
