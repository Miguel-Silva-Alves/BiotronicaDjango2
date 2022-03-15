from django.contrib import admin
from login.models import Device, Usuario, Cliente, Gateway
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario, UserAdmin)
admin.site.register(Cliente)
admin.site.register(Gateway)
admin.site.register(Device)

# Register your models here.
