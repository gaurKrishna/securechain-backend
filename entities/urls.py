from django.urls import path
from rest_framework import urlpatterns
from .views import AllowedReceivers, TemplateApi, EntityApi, InstanceApi, FlowApi, EntityBySupplychain, MySupplyChain
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r'template', TemplateApi)
router.register(r'entity', EntityApi)
router.register(r'instance', InstanceApi)
router.register(r'flow', FlowApi)

urlpatterns = [
    path("entitybysupplychain/", EntityBySupplychain.as_view(), name="entitybysupplychain"),
    path("mysupplychain/", MySupplyChain.as_view(), name="mysupplychain"),
    path("allowedreceivers/", AllowedReceivers.as_view(), name="allowedreceivers")
]

urlpatterns += router.urls