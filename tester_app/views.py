from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from tester_app.forms import ClientForm
from tester_app.models import Client

# General
def home(request):
    return render(request, 'home.html', {})
    
# Client
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    
    return render(request, 'client_form.html', {'form': form})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})
