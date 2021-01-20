from rest_framework import serializers
from wish_swap.tokens.models import Token, Dex


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'token_address',
            'fee_address',
            'fee',
            'decimals',
            'symbol',
            'network',
            'is_original',
        )


class DexSerializer(serializers.ModelSerializer):
    tokens = serializers.RelatedField(many=True)

    class Meta:
        model = Dex
        fields = ('tokens',)
