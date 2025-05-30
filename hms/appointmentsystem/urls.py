from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.home , name="home"),
    path('about/', views.about , name="about"),
    path('contact/', views.contact , name="contact"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.patient_signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page= 'home'), name="logout"),
    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/add_doctor/', views.add_doctor, name='add_doctor'),
    path('dashboard/display_doctors/', views.display_doctors, name='display_doctors'),
    path('dashboard/book_appointment/', views.book_appointment, name='book_appointment'),
    path('ajax/load-doctors/', views.load_doctors, name='ajax_load_doctors'),
    path('dashboard/appointments/', views.appointment_list, name='appointment_list'),
    path('dashboard/appointments/cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
    path('dashboard/register_admin/', views.register_admin, name='register_admin'),
    path('dashboard/requested_appointments/', views.requested_appointments, name='requested_appointments'),
    path('dashboard/requested_appointments/<int:request_id>/approve/', views.approve_appointment_request, name='approve_appointment_request'),
    path('dashboard/requested_appointments/<int:request_id>/reject/', views.reject_appointment_request, name='reject_appointment_request'),

    
    path('userdashboard/', views.user_dashboard, name='user_dashboard'),
    path('book/', views.book_online_appointment, name='book_online_app'),
    path('myappointments/', views.my_appointments, name='my_appointments'),
    path('update/<int:appointment_id>/', views.update_appointment, name='update_my_appointment'),
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),


]