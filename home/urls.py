from django.urls import path
from .views import *

urlpatterns = [
    path('home', homepage, name='home'),
    path('about',about,name='about'),
    path('pat_register',patient_register,name='register'),
    path('doctors',doctors_list, name='doctors'),
    path('book-appointment',book_appointment, name='booking'),
    path('my_appointments',my_appointments, name='my_appointments'),
    path('department',departments, name='department'),
    path('doc_dash',doctor_dashboard, name='doc_dash'),
    path('staff_dash',staff_dashboard, name='staff_dash'),
    path('status/<int:booking_id>/',status_approve, name='status_approve'),
    path('delete/<int:booking_id>/',delete_booking,name='delete_booking'),
    path('login/',Admin_login, name='login'),
    path('patient_login/',patient_login,name='patient_login'),
    path('patient_dash/',patient_dashboard, name='patient_dash'),
    path('logout/',logout_page, name='logout'),
    path('contact/',contact, name='contact'),
    
]