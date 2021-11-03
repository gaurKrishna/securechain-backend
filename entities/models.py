from django.db import models
from django.db.models.deletion import CASCADE
from django.views import generic
from authentication.models import User
from supplychain.models import SupplyChain


class Template(models.Model):
    template_name = models.CharField(max_length=255, blank=False, null=False)
    attributes = models.TextField(blank=False, null=False)


class Entity(models.Model):
    entity_name = models.CharField(max_length=255, blank=False, null=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="template")
    supply_chain = models.ForeignKey(SupplyChain, on_delete=models.CASCADE)


class Instance(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="parent_entity")
    ethereum_address = models.CharField(max_length=255, null=False, blank=True)
    connected_supply_chain = models.ForeignKey(
        SupplyChain, 
        on_delete=models.CASCADE, 
        related_name="instace_supply_chain", 
        blank=True, 
        null=True
    )
    connecting_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="connector_entity", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instance_user", blank=True, null=True)


class GenericAttributes(models.Model):
    TYPES = [
        ("Alphanumeric", "Alphanumeric"),
        ("String", "String"),
        ("Date", "Date"),
        ("Number", "Number")
    ]
    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(max_length=12, choices=TYPES, null=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, related_name="generic_attributes")


class GenericAttributeData(models.Model):
    data = models.CharField(max_length=255, null=False, blank=False)
    generic_attribute = models.ForeignKey(GenericAttributes, on_delete=models.CASCADE)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name="generic_attribute_data")

class Flow(models.Model):
    source = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="flow_source")
    destination = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="flow_destination")