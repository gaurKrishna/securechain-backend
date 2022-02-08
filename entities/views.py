import json
from enum import EnumMeta
from django.db.models.base import Model
from django.http.request import validate_host
from django.views import generic
from rest_framework import response
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from supplychain.models import SupplyChain
from .serializers import (
    SupplychainPKSerializer, 
    TemplateSerializer, 
    EntitySerializer, 
    InstanceSerializer, 
    GenericAttributesSerializer, 
    FlowSerializer,
)
from .models import Template, Entity, Instance, GenericAttributes, GenericAttributeData, Flow
from supplychain.serializers import SupplyChainSerializer
from supplychain.models import SupplyChain


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

    def list(self, request, *args, **kwargs):
        supply_chain = request.GET.get('supply_chain', None)

        if supply_chain:
            entities = Entity.objects.filter(supply_chain_id = supply_chain)
            response_data = EntitySerializer(entities, many=True).data

            return Response(response_data, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

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
    serializer_class = InstanceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # if request.user.role != "PARTICIPANT":
        #     return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        generic_attribute_data = serializer.validated_data.pop("generic_attribute_data")

        entity = serializer.validated_data.get("entity")

        generic_attributes = list(entity.generic_attributes.all())

        connected_supply_chain = serializer.validated_data.get("connected_supply_chain", None)

        connecting_entity = serializer.validated_data.get("connecting_entity", None)

        connected_flow = None
        if connected_supply_chain:
            if connecting_entity:
                connected_flow = Flow(source=entity, destination=connecting_entity)
            else:
                return Response({"error": "Connecting entity must be selected if you want to add your supply chain"}, status=status.HTTP_400_BAD_REQUEST)

            

        for gd in generic_attribute_data:
            if gd["generic_attribute"] not in generic_attributes:
                return Response(
                    {"Error": f"Generic attribute data passed must be from the generic attributes of the entity"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        instance = Instance.objects.create(**serializer.validated_data, user=request.user)
        
        if connected_flow:
            connected_flow.save()

        for gd in generic_attribute_data:
            gd["instance"] = instance
            GenericAttributeData.objects.create(**gd)

        return Response(
            {
                "Success": "Instance created successfully", 
                "data": InstanceSerializer(instance).data
            }, 
            status=status.HTTP_200_OK)
        

class FlowApi(ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, many=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for data in serializer.validated_data:
    
            source = data.get("source")
            destination = data.get("destination")

            if request.user != source.supply_chain.owner:
                return Response({"status": "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            if source.supply_chain != destination.supply_chain:
                return Response(
                    {"error": "The source and destination should beong to the same supply chain"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)

class EntityBySupplychain(APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = SupplychainPKSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        entities = Entity.objects.filter(supply_chain=serializer.validated_data.get("supply_chain"))

        response_data = EntitySerializer(entities, many=True)

        return Response(response_data.data, status=status.HTTP_200_OK)


class MySupplyChain(APIView):
    permission_classes = [IsAuthenticated]
    serializers_class = SupplyChain

    def get(self, request):
        my_supply_chain = SupplyChain.objects.filter(owner=request.user)
        response_data = SupplyChainSerializer(my_supply_chain, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)


class EnrolledSupplyChain(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplyChainSerializer

    def get(self, request):
        entities = Instance.objects.filter(user=request.user).values_list("entity", flat=True)
        supply_chain = SupplyChain.objects.filter(entity__in = entities)
        response_data = self.serializer_class(supply_chain, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)


class AllowedReceivers(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstanceSerializer

    def get(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data)

        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        pk = kwargs.get("pk", None)

        try:
            supply_chain = SupplyChain.objects.get(id=pk)
        except SupplyChain.DoesNotExist:
            return Response({"error": "Invalid supply chain id"}, status=status.HTTP_400_BAD_REQUEST)

        entities = Instance.objects.filter(user=request.user).values_list("entity" ,"entity__supply_chain")

        supply_chain_entity = []

        for entity, supply_chain_id in entities:
            if supply_chain_id == supply_chain.id:
                supply_chain_entity.append(entity)

        destination_entity = Flow.objects.filter(source_id__in = supply_chain_entity).values_list("destination", flat=True)

        destination_instances = Instance.objects.filter(entity__in = destination_entity)

        print(destination_instances)

        response_data = InstanceSerializer(destination_instances, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)

