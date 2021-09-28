from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import SupplyChain
from .serializers import SupplyChainSerializer


class SupplyChainAPI(ModelViewSet):
    queryset = SupplyChain.objects.all()
    serializer_class = SupplyChainSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != "OWNER":
            return Response({"unauthorized": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        data["owner"] = request.user

        supply_chain = SupplyChain.objects.create(**data)

        supply_chain = SupplyChainSerializer(supply_chain)

        return Response(supply_chain.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object
        if instance.owner == request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"unauthorized": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object
        if instance.owner == request.user:
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({"unauthorized": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object
        if instance.owner == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"unauthorized": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
