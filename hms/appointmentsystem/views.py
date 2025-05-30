from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientSignupForm, LoginForm , DoctorForm, AppointmentForm, AdminRegistrationForm, OnlineAppointmentForm
from django.contrib import messages
from .models import Doctor, Appointment, OnlineAppointmentRequest
 


def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

def contact(request):
    return render(request , 'contact.html')



def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = PatientSignupForm()

    context = {
        'form' : form
    }
    return render(request, 'signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email= email, password=password)

            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                if user.role == 'patient':
                    return redirect('user_dashboard')
                
            else:
                messages.error(request, "Invalid email or password")

    else:
        form = LoginForm()
    
    context = {
        'form' : form
    }
    return render(request, 'login.html', context)


# ADMIN DASHBOARD
def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.role == 'admin')(view_func)
    return decorated_view_func

@login_required(login_url='login')
@admin_required
def admin_dashboard(request):
    return render(request , 'admin/dashboard.html')

@login_required
@admin_required
def add_doctor(request):
    form = DoctorForm(request.POST , request.FILES)
    if form.is_valid():
        form.save()
        return redirect('display_doctors')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/add_doctor.html', context)

@login_required
@admin_required
def display_doctors(request):
    doctors = Doctor.objects.all()
    context = {
        'doctors' : doctors
    }
    return render(request, 'admin/display_doctors.html', context)

@login_required
@admin_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Appointment booked successfully.")
                return redirect('appointment_list')
            except IntegrityError:
                messages.error(request, "That time is already booked for this doctor.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AppointmentForm()

    context = {
        'form': form
    }
    return render(request, 'admin/book_appointment.html', context)

def load_doctors(request):
    department_id = request.GET.get('department')
    doctors = Doctor.objects.filter(department_id=department_id).values('id', 'full_name')
    return JsonResponse(list(doctors), safe=False)

@login_required
@admin_required
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    context = {
        'appointments': appointments
    }
    return render(request, 'admin/appointment_list.html', context)

@login_required
@admin_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Cancelled'
    appointment.save()
    messages.success(request, "Appointment cancelled successfully.")
    return redirect('appointment_list')

@login_required
@admin_required
def requested_appointments(request):
    requests = OnlineAppointmentRequest.objects.all().order_by('-submitted_at')
    context = {
        'requests': requests
    }
    return render(request, 'admin/requested_appointments.html', context)

@login_required
@admin_required
def approve_appointment_request(request, request_id):
    appointment_request = get_object_or_404(OnlineAppointmentRequest, id=request_id)
    if appointment_request.status != 'pending':
        return redirect('requested_appointments')

    # Create new Appointment
    Appointment.objects.create(
        full_name=appointment_request.full_name,
        email=appointment_request.email,
        phone=appointment_request.phone,
        department=appointment_request.department,
        doctor=appointment_request.doctor,
        appointment_date=appointment_request.date,
        appointment_time=appointment_request.time,
        description=appointment_request.description,
        status='Active',
    )

    # Update request status
    appointment_request.status = 'accepted'
    appointment_request.save()
    return redirect('requested_appointments')

@login_required
@admin_required
def reject_appointment_request(request, request_id):
    appointment_request = get_object_or_404(OnlineAppointmentRequest, id=request_id)
    if appointment_request.status == 'pending':
        appointment_request.status = 'rejected'
        appointment_request.save()
    return redirect('requested_appointments')

@login_required
@admin_required
def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # or a success page
    else:
        form = AdminRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'admin/register_admin.html', context)


# USER DASHBOARD
# @login_required
def user_dashboard(request):
    return render(request , 'user/p_dashboard.html')

@login_required
def book_online_appointment(request):
    if request.method == 'POST':
        form = OnlineAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('user_dashboard')  # Or to a success page
    else:
        form = OnlineAppointmentForm()

    context = {
        'form': form
    }
    
    return render(request, 'user/book_online_app.html', context)

@login_required
def my_appointments(request):
    appointments = OnlineAppointmentRequest.objects.filter(patient=request.user).order_by('-submitted_at')
    context = {
        'appointments': appointments
    }
    return render(request, 'user/my_appointments.html', context)


@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(OnlineAppointmentRequest, pk=appointment_id, patient=request.user)

    # Only allow updating if status is still 'pending'
    if appointment.status != 'pending':
        return redirect('my_appointments')

    if request.method == 'POST':
        form = OnlineAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('my_appointments')
    else:
        form = OnlineAppointmentForm(instance=appointment)

    context = {
        'form': form
    }

    return render(request, 'user/update_appointment.html', context)

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(OnlineAppointmentRequest, pk=appointment_id, patient=request.user)

    # Allow delete if status is pending, rejected or cancelled
    if appointment.status not in ['pending', 'rejected', 'cancelled']:
        return redirect('my_appointments')

    if request.method == 'POST':
        appointment.delete()
        return redirect('my_appointments')
    
    context = {
        'appointment': appointment
    }

    return render(request, 'user/delete_appointment.html', context)