from django.db import models


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return str(self.ip_address)
