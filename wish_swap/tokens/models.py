from django.db import models


class Secrets(models.Model):
    address = models.CharField(max_length=100)
    private = models.CharField(max_length=100)
    mnemonic = models.TextField()


class Dex(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __getitem__(self, network):
        return Token.objects.get(dex=self, network=network)


class Token(models.Model):
    dex = models.ForeignKey('tokens.Dex', on_delete=models.CASCADE, related_name='tokens')
    secrets = models.OneToOneField('tokens.Secrets', on_delete=models.SET_NULL, null=True)
    token_address = models.CharField(max_length=100)
    swap_address = models.CharField(max_length=100)
    fee_address = models.CharField(max_length=100)
    fee = models.IntegerField()
    decimals = models.IntegerField()
    symbol = models.CharField(max_length=50)
    network = models.CharField(max_length=100)
    is_original = models.BooleanField(default=False)
