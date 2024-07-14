from django import forms
from .models import WorkOrder
from contacts.models import Property, Service

class Select2MultipleCheckboxWidget(forms.SelectMultiple):
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',)
        }
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
              'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',)

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['contact', 'property', 'verify_address', 'evaluate_driveway', 'cover_condition', 'fluid_level', 'services']
        widgets = {
            'services': Select2MultipleCheckboxWidget(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property'].queryset = Property.objects.none()
        self.fields['services'].queryset = Service.objects.all()  # Ensure services queryset is set

        if 'contact' in self.data:
            try:
                contact_id = int(self.data.get('contact'))
                self.fields['property'].queryset = Property.objects.filter(contact_id=contact_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['property'].queryset = self.instance.contact.properties.all()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
