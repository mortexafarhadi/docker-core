from django.contrib import admin

from .models import models as mm

admin.site.register(mm.WalletWithdrawal)
