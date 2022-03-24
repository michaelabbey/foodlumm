from dataclasses import fields
import profile
from random import choice
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from foodie.models import *


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailInput()
        
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'message']
        
       
       
STATE = [
    ('Abia','Abia'),
    ('Abuja','Abuja'),
    ('Edo','Edo'),
    ('Kano','Kano'),
    ('Lagos','Lagos'),
    ('Ogun','Ogun'),
    ('Ph','Ph'),
]

COUNTRY = [
    ('Nigeria','Nigeria'),
    ('Dubia','Dubia'),
    ('United Kingdom','United Kingdom'),
    ('California','California'),
    ('Mexico','Mexico'),
]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'first_name', 'last_name', 'phone', 'address', 'state','country', 'image'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'state':forms.Select(attrs={'class':'form-control', 'placeholder':'State'}, choices=STATE),
            'country':forms.Select(attrs={'class':'form-control', 'placeholder':'Country'}, choices=COUNTRY),
            'image':forms.FileInput(attrs={'class':'form-control', 'placeholder':'Image'}),
        }

