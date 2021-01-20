from rest_framework import viewsets
from wish_swap.gas_info.models import GasInfo
from wish_swap.gas_info.serializers import GasInfoSerializer
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from wish_swap.tokens.models import Token


class GasInfoViewSet(viewsets.ModelViewSet):
    queryset = GasInfo.objects.all()
    serializer_class = GasInfoSerializer


fee_view_success_response = openapi.Response(
    description='amount of fee tokens',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'fee': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    )
)

fee_view_not_found_response = openapi.Response(
    description='response if no such token exists in db',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)


@swagger_auto_schema(
    method='post',
    operation_description='post token address and token network: '
                          '`Binance-Smart-Chain` or `Ethereum` and get fee amount',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'receive_token_address': openapi.Schema(type=openapi.TYPE_STRING),
            'receive_network': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['receive_token_address', 'receive_network']
    ),
    responses={200: fee_view_success_response, 404: fee_view_not_found_response}
)
@api_view(http_method_names=['POST'])
def fee_view(request):
    data = request.data
    try:
        token = Token.objects.get(token_address=data['receive_token_address'], network=data['receive_network'])
    except Token.DoesNotExist:
        return Response({'detail': 'no such token exists in db'}, 404)
    return Response({'fee': token.fee}, 200)
