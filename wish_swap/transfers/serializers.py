from rest_framework import serializers
from wish_swap.transfers.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    payment_hash = serializers.SerializerMethodField('get_payment_hash')
    payment_amount = serializers.SerializerMethodField('get_payment_amount')
    token_address = serializers.SerializerMethodField('get_token_address')
    network = serializers.SerializerMethodField('get_network')

    class Meta:
        model = Transfer
        fields = (
            'payment_hash',
            'address',
            'amount',
            'tx_hash',
            'token_address',
            'network',
            'status',
        )

    def get_payment_hash(self, transfer):
        return transfer.payment.tx_hash

    def get_payment_amount(self, transfer):
        return transfer.payment.amount

    def get_token_address(self, transfer):
        return transfer.token.token_address

    def get_network(self, transfer):
        return transfer.token.network
