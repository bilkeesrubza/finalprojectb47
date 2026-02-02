
from django.urls import path
from .views import *

urlpatterns = [
    path('home', homepage, name='home'),
    path('about',about,name='about'),
    path('doctors',doctors_list, name='doctors'),
    path('book-appointment',book_appointment, name='booking'),
    path('department',departments, name='department'),
    path('doc_dash',doctor_dashboard, name='doc_dash'),
    path('staff_dash',staff_dashboard, name='staff_dash'),
    path('status/<int:booking_id>/',status_approve, name='status_approve'),
    path('delete/<int:booking_id>/',delete_booking,name='delete_booking'),
    path('login/',login_view, name='login'),
    path('logout/',logout_page, name='logout'),
    path('contact/',contact, name='contact'),
    
]