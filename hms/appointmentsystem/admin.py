from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Department, Doctor, Appointment, OnlineAppointmentRequest

class PatientSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label='Full Name')
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(OnlineAppointmentRequest)


