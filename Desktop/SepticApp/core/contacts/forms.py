from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
from .models import Contact, Property, Payment, Appointment, Invoice, PropertyImage, ServiceContract, Document, Service
from django.forms import modelformset_factory


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['property', 'date', 'invoice_number', 'description', 'invoice_amount', 'amount_paid', 'balance']


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['contact']
        fields = [
         'address', 'township', 
            'parcel_number', 'permit_number', 'payment_owed'
        ]
        
    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({
            'id': 'id_address', 
            'class': 'form-control',
            'placeholder': 'Enter address'
        })
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'class': 'form-control-file',
        })

DocumentFormSet = modelformset_factory(Document, form=DocumentForm, extra=3)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_type', 'name','phone','email', 'address', 'tank_amount', 'tank_size', 'auto_email', 'preferred_contact_method']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        # Update widget attributes for all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Add specific attributes for the address field
        self.fields['address'].widget.attrs.update({
            'id': 'id_address',
            'placeholder': 'Enter address'
        })
  
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'job_volume', 'unit_price', 'property']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class Select2MultipleCheckboxWidget(forms.SelectMultiple):
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',)
        }
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
              'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['contact', 'property', 'tech', 'date_of_service', 'services']
        widgets = {
            'date_of_service': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'total': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['services'].queryset = Service.objects.all()

        if 'contact' in self.data:
            try:
                contact_id = int(self.data.get('contact'))
                self.fields['property'].queryset = Property.objects.filter(contact_id=contact_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['property'].queryset = self.instance.contact.properties.order_by('address')

        if 'services' in self.initial:
            self.fields['services'].initial = self.initial['services']

    def as_p(self):
        """Override the default rendering of the form to add `data-price` attributes to service options."""
        fields = super(InvoiceForm, self).as_p()
        # Render the services field with data-price attributes
        services_field = self['services']
        services_html = '<select multiple="multiple" name="services" class="form-control" id="id_services">'
        for service in services_field.field.queryset:
            selected = 'selected' if str(service.id) in self['services'].value() else ''
            services_html += f'<option value="{service.id}" data-price="{service.price}" {selected}>{service.name}</option>'
        services_html += '</select>'
        return fields.replace(str(self['services']), services_html)
    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None:
            raise forms.ValidationError('Total cannot be empty')
        return total
    
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'title']  # Include the title field
        labels = {
            'image': 'Upload Image',
            'title': 'Image Title'
        }

class ServiceContractForm(forms.ModelForm):
    class Meta:
        model = ServiceContract
        fields = ['job_name', 'total_tanks', 'total_price', 'service', 'frequency', 'first_service_date', 'end_date', 'job_notes']