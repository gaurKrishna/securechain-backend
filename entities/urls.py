from django.urls import path
from rest_framework import urlpatterns
from .views import TemplateApi, EntityApi, InstanceApi, FlowApi
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r'template', TemplateApi)
router.register(r'entity', EntityApi)
router.register(r'instance', InstanceApi)
router.register(r'flow', FlowApi)

urlpatterns = []

urlpatterns += router.urls