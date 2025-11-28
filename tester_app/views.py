import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from tester_app.forms import ClientForm, ProposalForm
from tester_app.models import Client, Proposal

from .utils.formatting import smart_title
import requests
from django.http import JsonResponse
import json

# General
def home(request):
    return render(request, 'home.html', {})


# Proposal
def update_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)

    if request.method == "POST":
        form = ProposalForm(request.POST, instance=proposal)

        if form.is_valid():

            # 1. Get JSON string from hidden input
            raw = form.cleaned_data.get("fiscal_year_end_data", "[]")

            # 2. Convert JSON → Python list of strings
            try:
                date_strings = json.loads(raw)
            except json.JSONDecodeError:
                date_strings = []

            # 3. Convert strings → actual Python date objects
            converted_dates = []
            for d in date_strings:
                try:
                    converted_dates.append(datetime.date.fromisoformat(d))
                except Exception:
                    pass  # ignore invalid dates

            # 4. Assign to the model’s ArrayField
            form.instance.fiscal_year_end = converted_dates

            base_fee = int(form.cleaned_data['base_fee'])
            assistance_fee = int(form.cleaned_data['assistance_fee'])
            ope_fee = int(form.cleaned_data['ope_fee'])

            # termin_values comes from a hidden field — JSON string
            percentages = form.cleaned_data['termin_values']

            # decode JSON array if needed
            if isinstance(percentages, str):
                try:
                    percentages = json.loads(percentages)
                except json.JSONDecodeError:
                    percentages = []

            total_fee = 0
            for p in percentages:
                subtotal = (base_fee + assistance_fee + ope_fee) * (p / 100)
                total_fee += subtotal

            # assign the final computed result
            form.instance.total_fee = int(total_fee)

            # save once only
            form.save()

            return redirect("proposal_list")

    else:
        form = ProposalForm(instance=proposal)

    existing_dates_json = json.dumps([
        d.isoformat() for d in proposal.fiscal_year_end
    ]) if proposal.fiscal_year_end else "[]"

    return render(request, 'proposal/proposal_form.html', {
        'form': form, 
        'form_title': 'Update Proposal',
        'existing_dates_json': existing_dates_json,
    })

def create_proposal(request):
    if request.method == "POST":
        form = ProposalForm(request.POST)
        
        if form.is_valid():

            # 1. Get JSON string from hidden input
            raw = form.cleaned_data.get("fiscal_year_end_data", "[]")

            # 2. Convert JSON → Python list of strings
            try:
                date_strings = json.loads(raw)
            except json.JSONDecodeError:
                date_strings = []

            # 3. Convert strings → actual Python date objects
            converted_dates = []
            for d in date_strings:
                try:
                    converted_dates.append(datetime.date.fromisoformat(d))
                except Exception:
                    pass  # ignore invalid dates

            # 4. Assign to the model’s ArrayField
            form.instance.fiscal_year_end = converted_dates

            # Recalculate total fee server-side to ensure integrity
            base_fee = int(form.cleaned_data['base_fee'])
            assistance_fee = int(form.cleaned_data['assistance_fee'])
            ope_fee = int(form.cleaned_data['ope_fee'])

            percentages = form.cleaned_data['termin_values']
            if isinstance(percentages, str):
                percentages = json.loads(percentages)

            total_fee = 0
            for p in percentages:
                subtotal = (base_fee + assistance_fee + ope_fee) * (p / 100)
                total_fee += subtotal

            form.instance.total_fee = int(total_fee)
            form.save()
            
            return redirect('proposal_list')
    
    else:
        form = ProposalForm()

    print(form.errors)
        
    return render(request, 'proposal/proposal_form.html', {'form': form, 'form_title': 'Create Proposal'})

def proposal_list(request):
    proposals = Proposal.objects.all()
    return render(request, 'proposal/proposal_list.html', {'proposals': proposals})


# Client
def wilayah_proxy(request, endpoint):
    url = f"https://emsifa.github.io/api-wilayah-indonesia/api/{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.province = smart_title(request.POST.get("province_name", ""))
            client.regency = smart_title(request.POST.get("regency_name", ""))
            client.district = smart_title(request.POST.get("district_name", ""))
            client.village = smart_title(request.POST.get("village_name", ""))
            client.save()
            return redirect('client_list')
    else:
        form = ClientForm()

    client = Client.objects.all()
    return render(request, 'client/client_form.html', {
        'form': form, 
        'client': client, 
        'form_title': 'Add Client'
    })

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client/client_list.html', {'clients': clients})

def update_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.province = smart_title(request.POST.get("province_name", ""))
            client.regency = smart_title(request.POST.get("regency_name", ""))
            client.district = smart_title(request.POST.get("district_name", ""))
            client.village = smart_title(request.POST.get("village_name", ""))
            client.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client/client_form.html', {'form': form, 'form_title': 'Update Client'})

def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'client/client_confirm_delete.html', {'client': client})
