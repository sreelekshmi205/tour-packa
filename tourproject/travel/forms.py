from django import forms
from django.contrib.auth.models import User
from .models import Package, Booking

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = ['vendor', 'created_at', 'approved']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package']
