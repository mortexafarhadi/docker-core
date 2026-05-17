from django.contrib import admin

from .models import models as mu

admin.site.register(mu.User)
