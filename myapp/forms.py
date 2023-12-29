# forms.py
from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['Username', 'Password', 'Email', 'DegreeProgramID']
# forms.py
from django import forms

class StudentLoginForm(forms.Form):
    Username = forms.CharField(max_length=255)
    Password = forms.CharField(widget=forms.PasswordInput)

