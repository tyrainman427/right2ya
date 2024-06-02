from django import forms
from .models import Contract 


# Create your forms here.
class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = "__all__"
        exclude = ['total_price']
