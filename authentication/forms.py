from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': '',
            'name': "username", 
            'id': "username", 
            'type': "text", 
            'class': "form-input", 
            'placeholder': "username", 
            'maxlength': "16", 
            'minlength': "6"
        })
        self.fields['email'].widget.attrs.update({
            'required': '',
            'name': "email", 
            'id': "email", 
            'type': "email", 
            'class': "form-input", 
            'placeholder': "email", 
        })
        self.fields['password1'].widget.attrs.update({
            'required': '',
            'name': "password1", 
            'id': "password1", 
            'type': "password", 
            'class': "form-input", 
            'placeholder': "password", 
            'maxlength': "22", 
            'minlength': "8"
        })
        self.fields['password2'].widget.attrs.update({
            'required': '',
            'name': "password2", 
            'id': "password2", 
            'type': "password", 
            'class': "form-input", 
            'placeholder': "confirm password", 
            'maxlength': "22", 
            'minlength': "8"
        })







    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
