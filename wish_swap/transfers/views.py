from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from wish_swap.payments.models import Payment
from wish_swap.transfers.serializers import TransferSerializer
from wish_swap.transfers.models import Transfer
from rest_framework.views import APIView


payment_not_found_response = openapi.Response(
    description='response if no such payment exists in db',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)


class TransferView(APIView):
    @swagger_auto_schema(
        operation_description="Get transfer info by payment hash\n"
                              "Transfer statuses: `SUCCESS`, `HIGH GAS PRICE`, "
                              "`FAIL` or `DECLINED` (of fee is more then token amount)",
        manual_parameters=[
            openapi.Parameter('payment_hash', openapi.IN_PATH, type=openapi.TYPE_STRING),
        ],
        responses={200: TransferSerializer(), 404: payment_not_found_response},
    )
    def get(self, request, payment_hash):
        try:
            payment = Payment.objects.get(tx_hash=payment_hash)
        except Payment.DoesNotExist:
            return Response({'detail': 'no such payment exists in db'}, 404)
        transfer = Transfer.objects.get(payment=payment)
        serializer = TransferSerializer(transfer)
        return Response(serializer.data, status=200)
