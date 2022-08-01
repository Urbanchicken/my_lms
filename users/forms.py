from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'std_number','first_name', 'last_name', 'email', 'role', 'profile_picture')