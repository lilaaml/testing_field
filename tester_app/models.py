from django.db import models
from django.contrib.postgres.fields import ArrayField

class Client(models.Model):
    name = models.CharField(max_length=255) # Client Name
    street = models.CharField(max_length=255, null=True, blank=True) # Street Name
    province = models.CharField(max_length=255, null=True, blank=True) # Provinsi
    regency = models.CharField(max_length=255, null=True, blank=True) # Kabupaten / Kota
    district = models.CharField(max_length=255, null=True, blank=True) # Kecamatan
    village = models.CharField(max_length=255, null=True, blank=True) # Kelurahan
    products = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True
    )

    def __str__(self):
        return f"{ self.name }"