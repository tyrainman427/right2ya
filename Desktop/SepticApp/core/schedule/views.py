from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, authenticate  
from contacts.forms import AppointmentForm  
from django.http import JsonResponse
from contacts.models import  Appointment

def appointment_data(request):
    appointments = Appointment.objects.all()  # Fetch your appointments
    appointment_list = [{
        'customer': appt.user.first_name,  # Replace with your appointment fields
        'start': appt.date.isoformat(),  # Ensure datetime is ISO format
        'id': appt.id
  
    } for appt in appointments]
    return JsonResponse(appointment_list, safe=False)

# Create your views here.
def schedule_home(request):
    return render(request, 'schedule/home.html')


def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property
            appointment.user = request.user 
            appointment.save()
            return redirect('schedule_appointment', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})
