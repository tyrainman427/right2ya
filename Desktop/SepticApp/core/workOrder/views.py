from django.shortcuts import render, redirect, get_object_or_404
from .models import WorkOrder
from .forms import WorkOrderForm
from django.http import JsonResponse
from contacts.models import Property, Invoice
from django.contrib.auth.decorators import login_required
from contacts.forms import InvoiceForm
from decimal import Decimal

@login_required
def work_order_detail(request, order_id):
    order = get_object_or_404(WorkOrder, id=order_id)
    return render(request, 'work_order_detail.html', {'order': order})

@login_required
def complete_work_order(request, order_id):
    order = get_object_or_404(WorkOrder, id=order_id)
    if request.method == 'POST':
        order.is_completed = True
        order.save()
        return redirect('work_order_detail', order_id=order.id)
    return redirect('work_order_detail', order_id=order.id)

@login_required
def create_invoice_from_work_order(request, order_id):
    order = get_object_or_404(WorkOrder, id=order_id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.contact = order.contact
            invoice.property = order.property
            invoice.date_of_service = order.date_of_service

            last_invoice = Invoice.objects.all().order_by('id').last()
            if last_invoice and last_invoice.invoice_number and last_invoice.invoice_number.isdigit():
                invoice.invoice_number = str(int(last_invoice.invoice_number) + 1)
            else:
                invoice.invoice_number = '1000'

            invoice.save()
            form.save_m2m()

            # Calculate the total after saving the services
            services = invoice.services.all()
            subtotal = sum(service.price for service in services)
            serviceFee = subtotal * Decimal('0.15')
            invoice.total = subtotal + serviceFee
            invoice.save()

            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        initial_data = {
            'contact': order.contact,
            'property': order.property,
            'date_of_service': order.date_of_service,
            'services': order.services.all(),
        }
        form = InvoiceForm(initial=initial_data)
    return render(request, 'contacts/create_invoice.html', {'form': form, 'order': order})

@login_required
def create_work_order(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            work_order = form.save(commit=False)
            
            # Generate the next work order number
            last_work_order = WorkOrder.objects.all().order_by('id').last()
            if last_work_order and last_work_order.work_order_number and last_work_order.work_order_number.isdigit():
                work_order.work_order_number = str(int(last_work_order.work_order_number) + 1)
            else:
                work_order.work_order_number = '3000'
            
            # Save the work order instance
            work_order.save()
            
            # Save the many-to-many relationship for services
            form.save_m2m()
            
            return redirect('work_order_list')
        else:
            print("Form errors:", form.errors)  # Debugging statement
    else:
        form = WorkOrderForm()
    return render(request, 'create_work_order.html', {'form': form})

@login_required
def ajax_load_properties(request):
    contact_id = request.GET.get('contact_id')
    properties = Property.objects.filter(contact_id=contact_id).all()
    return JsonResponse({'properties': [{'id': prop.id, 'address': prop.address} for prop in properties]})

@login_required
def work_home(request):
    pass

@login_required
def work_order_list(request):
    orders = WorkOrder.objects.all()
    return render(request, 'work_order_list.html', {'orders': orders})
