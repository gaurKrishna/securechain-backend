from enum import EnumMeta
from django.db.models.base import Model
from rest_framework import response
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from .serializers import TemplateSerializer, EntitySerializer, InstanceSerialzer, GenericAttributesSerializer
from .models import Template, Entity, Instance, GenericAttributes


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

        entity = Entity.objects.create(**serializer.validated_data)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        suppl_chain = instance.supply_chain

        if request.user != suppl_chain.owner:
            return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(instance)

        return Response({"status": "Entity delete successfully"}, status=status.HTTP_200_OK)
