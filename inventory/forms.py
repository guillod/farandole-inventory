from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput, DateInput

from .models import Object

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'

class ObjectForm(forms.ModelForm):

    class Meta:
        model = Object
        fields = ['description','nb','group','location','state','photo','supplier','price', 'buy_at','comment']
        widgets = {
            'photo': CustomClearableFileInput(attrs={'capture':'environment', 'accept':'image/*'}),
            'buy_at': DateInput(attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ObjectForm, self).__init__(*args, **kwargs)
        if self.instance.buy_at:
            self.initial['buy_at'] = self.instance.buy_at.isoformat()
