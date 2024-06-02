from django.shortcuts import get_object_or_404,redirect, render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import DocumentForm
from .filters import ClientFilter

# Create your views here.
class ClientList(ListView):
    model = Client
    template_name = 'clients/clients_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ClientFilter(self.request.GET, queryset=self.get_queryset())
        return context

class ClientCreateView(CreateView):
    model = Client
    fields = ['first_name','last_name','address','phone',
    'date_of_birth','client_id','medicaid_id','csp_contact_info',
    'referring_clinician','cop_name_and_number','service_days','service_hours',
    'intake_completed_by','date','start_date'
    ]


class UploadFileView(CreateView):
    model = Document
    fields = ['client','user','title','docs']

class NotesCreateView(CreateView):
    model = Note
    fields = '__all__'



class ClientDetailView(DetailView):
    template_name = "clients/clients_detail.html"
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)

        context['note'] = Note.objects.all()
        context['document'] = Document.objects.all()
        return context

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)


class NoteDetailView(DetailView):
    template_name = "clients/note_detail.html"
    model = Note

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Note, id=id_)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['first_name','last_name','address','phone',
    'date_of_birth','client_id','medicaid_id','csp_contact_info',
    'referring_clinician','cop_name_and_number','service_days','service_hours',
    'intake_completed_by','date','start_date'
    ]

    def get_absolute_url(self):
        return reverse('clients:file_detail', args=[str(self.id)])

class ClientDeleteView(DeleteView):
    model = Client
    success_url = '/clients/'
