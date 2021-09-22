from django.db import models
from authentication.models import User
from supplychain.models import SupplyChain


class Template(models.Model):
    template_name = models.CharField(max_length=255, blank=False, null=False)
    attributes = models.TextField(blank=False, null=False)


class Entity(models.Model):
    entity_name = models.CharField(max_length=255, blank=False, null=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="template")
    supply_chain = models.ForeignKey(SupplyChain, on_delete=models.CASCADE)
    attributes = models.TextField(blank=False, null=False)


class Instance(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)


class GenericAttributes(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    value = models.TextField(blank=False, null=False)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)