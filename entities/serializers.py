from django.db.models.base import Model
from rest_framework.serializers import ModelSerializer
from .models import Template, Entity, Instance, GenericAttributes


class TemplateSerializer(ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class EntitySerializer(ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class InstanceSerialzer(ModelSerializer):
    class Meta:
        model = Instance
        fields = "__all__"


class GenericAttributesSerializer(ModelSerializer):
    class Meta:
        model = GenericAttributes
        fields = "__all__"