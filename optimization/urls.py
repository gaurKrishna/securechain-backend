from django.urls import path
from rest_framework import urlpatterns

from .views import OptimizationApi

urlpatterns = [
    path("optimization/<int:supplychain>/<int:entity>", OptimizationApi.as_view(), name="optimizationapi"),
]