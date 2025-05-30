from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_User(self, email, full_name, password=None, role='patient', **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_User(email, full_name, password, role='admin', **extra_fields)


class CustomUser(AbstractUser):
    username = None  # disable default username
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # use email as the unique login

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # required when using createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email 


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name 
    

class Doctor(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class OnlineAppointmentRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.full_name} with {self.doctor} on {self.date} at {self.time} ({self.status})"
    
class Appointment(models.Model):
    full_name =  models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')  # Prevent double booking

    def _str_(self):
        return f"{self.full_name} - {self.appointment_date} at {self.appointment_time} - {self.status}"