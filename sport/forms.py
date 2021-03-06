from django.forms import ModelForm
from django import forms
from .models import *
from bootstrap_datepicker_plus import DatePickerInput

class PlayerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  
        super(PlayerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Player
        # fields = '__all__'
        exclude = ['registeration_date', 'qr_code']        
        widgets = {
            'first_name' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'mobile' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'address' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'required': True, 'class': 'form-control'}),
            'gender' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'plus21' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            # 'plus21' : forms.CheckboxInput(attrs={'class' : 'custom-checkbox checkbox-xl', 'required': False}),
            'date_of_birth' : DatePickerInput(format='%m/%d/%Y'),
            # 'date_of_birth' : forms.DateField(required= False, widget=DatePickerInput(format='%m/%d/%Y')),
            'vaccinated' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            # 'vaccinated' : forms.CheckboxInput(attrs={'class' : 'custom-checkbox checkbox-xl'}),
            'emergency_contact_name' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'emergency_contact_phone' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'profile_picture' : forms.ClearableFileInput(attrs={'required': True, 'class': 'form-control'}),
            'disclaimer' : forms.CheckboxInput(attrs={'required': True, 'class' : 'custom-checkbox checkbox-xl'})
        }

        labels = {
            "plus21" : "Are you 21+ age ? ",
            "vaccinated" : "Are you vaccinated ? ",
            "disclaimer" : "Release of Liability and COVID-19 Related Information (Required)",
            "profile_picture" : "Attach a clear image of your face. Please do not attach avatar image! "
        }   


class ScannerForm(forms.Form):
    ID = forms.CharField(max_length=100, required=True)
     
        