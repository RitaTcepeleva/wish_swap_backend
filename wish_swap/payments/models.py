from django.db import models


class Payment(models.Model):
    token = models.ForeignKey('tokens.Token', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    tx_hash = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=100, decimal_places=0)
    transfer_address = models.CharField(max_length=100)
    transfer_network_number = models.IntegerField()
    validation_status = models.CharField(max_length=100, default='WAITING FOR VALIDATION')
