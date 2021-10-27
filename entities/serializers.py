from django.db.models.base import Model
from django.db.models.query import QuerySet
from rest_framework import fields
from rest_framework import serializers 
from .models import Template, Entity, Instance, GenericAttributes, GenericAttributeData, Flow
from supplychain.models import SupplyChain


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class GenericAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericAttributes
        fields = "__all__"


class EntitySerializer(serializers.ModelSerializer):
    generic_attributes = GenericAttributesSerializer(many=True)
    class Meta:
        model = Entity
        fields = "__all__"


class GenericAttributeDataSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source="generic_attribute.name", read_only=True)
    attribute_type = serializers.CharField(source="generic_attribute.type", read_only=True)
    class Meta:
        model = GenericAttributeData
        fields = "__all__"
        read_only_fields = ["instance"]


class InstanceSerializer(serializers.ModelSerializer):
    generic_attribute_data = GenericAttributeDataSerializer(many=True)
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