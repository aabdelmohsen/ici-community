from django.forms import ModelForm
from django import forms
from .models import *
from bootstrap_datepicker_plus import DatePickerInput

class PlayerForm(ModelForm):
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
            'gender' : forms.RadioSelect(),
            # 'date_of_birth' : forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/yyyy'}),
            'date_of_birth' : DatePickerInput(format='%m/%d/%Y'),
            'vaccinated' : forms.CheckboxInput(attrs={'class' : 'custom-checkbox checkbox-xl'}),
            'emergency_contact_name' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'emergency_contact_phone' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'profile_picture' : forms.ClearableFileInput(attrs={'required': True, 'class': 'form-control'})
        }

        labels = {
            "vaccinated": "Check if you are vaccinated "
        }   
