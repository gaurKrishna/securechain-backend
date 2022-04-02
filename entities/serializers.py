from django.db.models.base import Model
from django.db.models.query import QuerySet
from rest_framework import fields
from rest_framework import serializers 
from .models import Template, Entity, Instance, Flow
from supplychain.models import SupplyChain


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = "__all__"
        read_only_fields = ["user"]


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = "__all__"


class SupplychainPKSerializer(serializers.Serializer):
    supply_chain = serializers.PrimaryKeyRelatedField(queryset = SupplyChain.objects.all())