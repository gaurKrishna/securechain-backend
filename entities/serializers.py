from django.db.models.base import Model
from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from .models import Template, Entity, Instance, GenericAttributes, GenericAttributeData


class TemplateSerializer(ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class GenericAttributesSerializer(ModelSerializer):
    class Meta:
        model = GenericAttributes
        fields = "__all__"


class EntitySerializer(ModelSerializer):
    generic_attributes = GenericAttributesSerializer(many=True)
    class Meta:
        model = Entity
        fields = "__all__"


class GenericAttributeDataSerializer(ModelSerializer):
    class Meta:
        model = GenericAttributeData
        fields = "__all__"


class InstanceSerialzer(ModelSerializer):
    generic_attribute_data = GenericAttributeDataSerializer(many=True)
    class Meta:
        model = Instance
        fields = "__all__"