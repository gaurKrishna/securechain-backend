from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import SupplyChain


class SupplyChainSerializer(ModelSerializer):
    class Meta:
        model = SupplyChain
        fields = "__all__" 