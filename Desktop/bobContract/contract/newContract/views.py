from django.shortcuts import render, redirect
from .models import Contract
from .forms import ContractForm
from django.contrib import messages
from django.views.generic.detail import DetailView


# Create your views here.
def contract(request):
    photos = 100
    lights = 75
    time = 50
    base = 300
    total = 0
    
    if request.method == 'POST':
        contract_form = ContractForm(request.POST, request.FILES)
        if contract_form.is_valid(): 
            if Contract.add_photos and Contract.add_lights and Contract.add_more_time:
                total = base + lights + photos + time
            else:
                total = base
            
            total = contract_form.cleaned_data['total_price']
            contract_form.save()
            
        return redirect("newContract:contract")
    
	# 		messages.success(request, ('Your contract was successfully added!'))
    #     else:
    #         messages.error(request, 'Error saving form')
    
    contract_form = ContractForm()
    contracts = Contract.objects.all()
     
	
    return render(request=request, template_name="newContract/contract.html", context={'contract_form':contract_form, 'contracts':contracts,
                                                                                    'photos':photos,'lights':lights,'time':time,'base':base,
                                                                                    'total':total
                                                                                    })

class ContractDetailView(DetailView):
    model = Contract

def index(request):
    return render(request, 'newContract/index.html')

