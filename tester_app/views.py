from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from tester_app.forms import ClientForm
from tester_app.models import Client

from .utils.formatting import smart_title
import requests
from django.http import JsonResponse

# General
def home(request):
    return render(request, 'home.html', {})
    
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
    return render(request, 'client_form.html', {
        'form': form, 
        'client': client, 
        'form_title': 'Add Client'
    })

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def update_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_form.html', {'form': form, 'form_title': 'Update Client'})

def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'client_confirm_delete.html', {'client': client})
