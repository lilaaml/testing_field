from django import forms
from .models import Client, Proposal, Temp
import json

class ClientForm(forms.ModelForm):
    # Hidden field to receive the final combined list
    products_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Client
        fields = ['name', 'street', 'province', 'regency', 'district', 'village', 'products_data']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'class': 'form-control',
            }),
            'street': forms.TextInput(attrs={
                'id': 'street',
                'class': 'form-control',
            }),
            'province': forms.Select(attrs={
                'id': 'province',
                'class': 'form-control',
            }),
            'regency': forms.Select(attrs={
                'id': 'regency',
                'class': 'form-control',
            }),
            'district': forms.Select(attrs={
                'id': 'district',
                'class': 'form-control',
            }),
            'village': forms.Select(attrs={
                'id': 'village',
                'class': 'form-control',
            }),
        }
    
    def clean(self):
        cleaned = super().clean()

        raw = cleaned.get('products_data', '')

        # Convert JSON string → list
        try:
            products = json.loads(raw)
        except:
            products = []

        cleaned['products'] = products
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.products = self.cleaned_data['products']
        if commit:
            instance.save()
        return instance

        
class ProposalForm(forms.ModelForm):
    # Hidden field to receive the final combined list
    fiscal_year_end_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Proposal
        fields = ['client', 'audit_type', 'fiscal_year_end']

        widgets = {
            'client': forms.Select(attrs={
                'id': 'client',
                'class': 'form-select',
            }),
            'audit_type': forms.Select(attrs={
                'id': 'audit_type',
                'class': 'form-control',
            }),
        }

    def clean(self):
        cleaned = super().clean()

        raw = cleaned.get('fiscal_year_end_data', '')

        # Convert JSON string → list
        try:
            fiscal_year_end = json.loads(raw)
        except:
            fiscal_year_end = []

        cleaned['fiscal_year_end'] = fiscal_year_end
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.fiscal_year_end = self.cleaned_data['fiscal_year_end']
        if commit:
            instance.save()
        return instance

class TempForm(forms.ModelForm):
    temp_date = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Temp
        fields = ['temp_id', 'temp_select', 'temp_date']
        widgets = {
            'temp_id': forms.TextInput(attrs={
                'id': 'temp_id',
                'class': 'form-select',
            }),
            'temp_select': forms.Select(attrs={
                'id': 'temp_select',
                'class': 'form-select',
            }),
        }

    def clean(self):
        cleaned = super().clean()

        raw = cleaned.get('temp_date', '')

        # Convert JSON string → list
        try:
            temp_date = json.loads(raw)
        except:
            temp_date = []

        cleaned['temp_date'] = temp_date
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.temp_date = self.cleaned_data['temp_date']
        if commit:
            instance.save()
        return instance