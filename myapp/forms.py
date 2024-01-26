# forms.py
from django import forms
from .models import Student

from django import forms

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['Username', 'Password', 'Email', 'DegreeProgramID']

        widgets = {
            'Username': forms.TextInput(attrs={'class': 'form-control'}),
            'Password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'DegreeProgramID': forms.Select(attrs={'class': 'form-control'}),
        }


class StudentLoginForm(forms.Form):
    Username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
