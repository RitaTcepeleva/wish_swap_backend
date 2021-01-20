from rest_framework import viewsets
from wish_swap.gas_info.models import GasInfo
from wish_swap.gas_info.serializers import GasInfoSerializer


class GasInfoViewSet(viewsets.ModelViewSet):
    queryset = GasInfo.objects.all()
    serializer_class = GasInfoSerializer
