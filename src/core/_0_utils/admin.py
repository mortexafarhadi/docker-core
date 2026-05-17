from django.contrib import admin

from .models import ip_address_model as mm

admin.site.register(mm.IPAddress)
