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
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)


class GenericAttributes(models.Model):
    TYPES = [
        ("Numeric", "Numeric"),
        ("String", "String"),
        ("Date", "Date")
    ]
    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(max_length=8, choices=TYPES, null=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, related_name="generic_attributes")


class GenericAttributeData(models.Model):
    data = models.CharField(max_length=255, null=False, blank=False)
    generic_attribute = models.ForeignKey(GenericAttributes, on_delete=models.CASCADE)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name="generic_attribute_data")

class Flow(models.Model):
    source = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="flow_source")
    destination = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="flow_destination")