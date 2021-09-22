from django.urls import path
from rest_framework import urlpatterns
from .views import TemplateApi, EntityApi
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r'template', TemplateApi)
router.register(r'entity', EntityApi)

urlpatterns = []

urlpatterns += router.urls