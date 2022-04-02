from django.db import models
from django.db.models.deletion import CASCADE
from django.views import generic
from authentication.models import User
from supplychain.models import SupplyChain


class Template(models.Model):
    template_name = models.CharField(max_length=255, blank=False, null=False)
    attributes = models.JSONField(blank=True, null=True)


class Entity(models.Model):
    entity_name = models.CharField(max_length=255, blank=False, null=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="template")
    supply_chain = models.ForeignKey(SupplyChain, on_delete=models.CASCADE)
    generic_attributes = models.JSONField(blank=True, null=True)


class Instance(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="parent_entity")
    ethereum_address = models.CharField(max_length=255, blank=False, null=False)
    connected_supply_chain = models.ForeignKey(
        SupplyChain,
        on_delete=models.CASCADE,
        related_name="instace_supply_chain",
        blank=True,
        null=True
    )
    connecting_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="connector_entity", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instance_user", blank=True, null=True)
    generic_attributes_data = models.JSONField(blank=True, null=True)

class Flow(models.Model):
    source = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="flow_source")
    destination = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="flow_destination")