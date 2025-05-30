from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Doctor, Appointment, OnlineAppointmentRequest

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

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
    

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        # fields = ['full_name', 'email', 'phone', 'department', 'specialization']
        exclude = ['registration_date']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['submitted_at', 'status']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id': 'id_date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'id': 'id_time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class OnlineAppointmentForm(forms.ModelForm):
    class Meta:
        model = OnlineAppointmentRequest
        exclude = ['submitted_at', 'status', 'patient']

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if doctor and date and time:
            exists = OnlineAppointmentRequest.objects.filter(
                doctor=doctor,
                date=date,
                time=time
            ).exclude(status='rejected').exists()
            if exists:
                raise forms.ValidationError("This time slot is already booked for the selected doctor.")
        return cleaned_data