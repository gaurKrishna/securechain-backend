from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import SupplyChainAPI

router = SimpleRouter()

router.register(r'supplychain', SupplyChainAPI)

urlpatterns = []

urlpatterns += router.urls