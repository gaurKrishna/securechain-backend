import json
from enum import EnumMeta
from django.db.models.base import Model
from django.http.request import validate_host
from django.views import generic
from rest_framework import response
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from .serializers import TemplateSerializer, EntitySerializer, InstanceSerialzer, GenericAttributesSerializer
from .models import Template, Entity, Instance, GenericAttributes, GenericAttributeData


class TemplateApi(ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class EntityApi(ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        supply_chain = serializer.validated_data.get("supply_chain") 

        if request.user != supply_chain.owner:
            return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        generic_attributes = serializer.validated_data.pop("generic_attributes")
        generic_attributes = [dict(generic_attribute) for generic_attribute in generic_attributes]
        
        template = serializer.validated_data.get("template")
        template = template.attributes.split(";")
        template = [json.loads(temp) for temp in template]

        for temp in template:
            generic_attributes.append(temp)
        
        entity = Entity.objects.create(**serializer.validated_data)

        for generic_attribute in generic_attributes:
            generic_attribute["entity"] = entity
            generic_attribute = GenericAttributes.objects.create(**generic_attribute)

        serializer = self.serializer_class(entity)

        return Response(
            {
                "status": "Entity Created Successfully",
                "data": serializer.data
            }, status = status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        supply_chain = serializer.validated_data.get("supply_chain")

        if request.user != supply_chain.owner:
            return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(
            {
                "status": "Updated successfully",
                "data": serializer.data     
            }, status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        supply_chain = serializer.validated_data.get("supply_chain")

        if request.user != supply_chain.owner:
            return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(
            {
                "status": "Updated successfully",
                "data": serializer.data     
            }, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        suppl_chain = instance.supply_chain

        if request.user != suppl_chain.owner:
            return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(instance)

        return Response({"status": "Entity delete successfully"}, status=status.HTTP_200_OK)


class InstanceApi(ModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerialzer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.role != "PARTICIPANT":
            return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        generic_attribute_data = serializer.validated_data.get("generic_attributes_data")



