from django.db import models
from authentication.models import User

class SupplyChain(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chain_owner")
    date_created = models.DateField(auto_now_add=True)