from django import template
from django.utils import timezone

register = template.Library()

MONTHS_ID = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

@register.filter
def fiscal_date_id(value):
    if not value:
        return ""
    return f"{value.day} {MONTHS_ID[value.month]} {value.year}"