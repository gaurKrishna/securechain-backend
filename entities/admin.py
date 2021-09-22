from django.contrib import admin
from .models import Template, Entity, Instance, GenericAttributes


admin.site.register(Template)
admin.site.register(Entity)
admin.site.register(Instance)
admin.site.register(GenericAttributes)