from django.db import models
from encrypted_fields import fields


class Dex(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __getitem__(self, network):
        return Token.objects.get(dex=self, network=network)


class Token(models.Model):
    dex = models.ForeignKey('tokens.Dex', on_delete=models.CASCADE, related_name='tokens')
    token_address = models.CharField(max_length=100)
    token_abi = models.JSONField(null=True, default=None)
    swap_address = models.CharField(max_length=100)
    swap_owner = models.CharField(max_length=100, default='')
    swap_abi = models.JSONField(null=True, default=None)
    swap_secret = fields.EncryptedTextField(default='')  # private key for Ethereum-like, mnemonic for Binance-Chain
    fee_address = models.CharField(max_length=100)
    fee = models.IntegerField()
    decimals = models.IntegerField()
    symbol = models.CharField(max_length=50)
    network = models.CharField(max_length=100)
    is_original = models.BooleanField(default=False)
