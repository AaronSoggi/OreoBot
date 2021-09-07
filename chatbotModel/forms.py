from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User



class studentForm(UserCreationForm):
   
        username = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={
            'autocomplete':'off', 'class': 'user_input', 'placeholder' : 'Username'
        }))
        
        email = forms.CharField(max_length = 100, widget = forms.EmailInput(attrs={
            'class': 'user_input', 'placeholder' : 'Email address'
        }))

        password1 = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={
            'class': 'user_input', 'placeholder' : 'Password' 
        }))

        password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={
            'class': 'user_input', 'placeholder' : 'Confirm password' 
        }))
        
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']


        


        