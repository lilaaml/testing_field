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
    

class Proposal(models.Model):
    proposal_id = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="proposal")
    audit_type = models.CharField(
        max_length=255,
        choices=[
            ('Tahunan', 'Tahunan'),
            ('IPO', 'IPO'),
            ('Interim - Audit', 'Interim - Audit'),
            ('Interim - Review', 'Interim - Review'),
            ('Non-Audit Umum', 'Non-Audit Umum'),
        ]
    )
    fiscal_year_end = ArrayField(
        models.DateField(),
        default=list,
        blank=True
    )
    base_fee = models.PositiveIntegerField()  # report audit / report / audit
    assistance_fee = models.PositiveIntegerField()  # ipo assistance 
    ope_fee = models.PositiveIntegerField()  # out of pocket fee
    sub_fee = models.PositiveIntegerField()  # base + assist + ope 
    total_fee = models.PositiveIntegerField(null=True)  # sub * percentage
    num_termins = models.PositiveIntegerField()
    termin_values = models.JSONField()  # [50,50] [30,40,30] [25,25,25,25]
    total_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{ self.proposal_id }"