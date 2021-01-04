from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from wish_swap.rates.api import calculate_wish_fee
from wish_swap.settings import TOKEN_DECIMALS


success_response = openapi.Response(
    description='transaction fee in WISH',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'wish_fee': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    )
)


@swagger_auto_schema(
    method='post',
    operation_description='post amount of tokens you want to exchange, '
                          'address and blockchain for sending tokens: '
                          '`Binance-Chain`, `Binance-Smart-Chain` or `Ethereum`',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'to_blockchain': openapi.Schema(type=openapi.TYPE_STRING),

        },
        required=['amount', 'address', 'to_blockchain']
    ),
    responses={200: success_response}
)
@api_view(http_method_names=['POST'])
def wish_fee_view(request):
    data = request.data
    wish_fee = calculate_wish_fee(data['to_blockchain'], data['address'], data['amount'] * TOKEN_DECIMALS)
    return Response({'wish_fee': wish_fee / TOKEN_DECIMALS}, 200)
