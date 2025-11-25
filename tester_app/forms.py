from django import forms
from .models import Client
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

        
