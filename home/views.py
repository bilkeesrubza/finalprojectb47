from urllib import request
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Doctors,DoctorUser,Departments,Booking,UserProfile
from .forms import *
from django.contrib import messages
from django.utils import timezone


# Create your views here.
#------GENERAL VIEWS----------------
def about(request):
    return render(request,'welcome.html',{'show_navbar': False})

def logout_page(request):
    logout(request)
    return render(request,'welcome.html')

def contact(request):
    return render(request,'contact.html')

def homepage(request):
    return render(request,'home.html')

def departments(request):
    doc_dept={
        'dept':Departments.objects.all()
    }
    return render(request,'department.html',doc_dept)


def doctors_list(request):
    doctors={
        'doc':Doctors.objects.all()}
    return render(request,'doctor.html',doctors)


    

                                        #------USER FIELDS AND VIEWS--------------------

#-----FOR PATIENT REGISTRATION----------------
def patient_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone']
            )

            messages.success(
                request,
                "Registration successful. Please login to continue."
            )
            return redirect('about')   # login page

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

#------FOR PATIENT LOGIN----------------

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if DoctorUser.objects.filter(user=user).exists() or user.is_staff:
                return render(request, 'welcome.html', {'error': "You are not authorized to login here."})
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("patient_dash")
        else:
            messages.error(request, "You entered wrong username or password")
    return render(request, "welcome.html",{'show_navbar': False})



#------FOR BOOKING APPOINTMENT----------------

@login_required
def book_appointment(request):

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return render(request, 'success.html')
        else:
            messages.error(request, "Invalid Input Data")
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})





#------FOR PATIENT DASHBOARD----------------
@login_required
def patient_dashboard(request):
    today = timezone.now().date()
    appointments = Booking.objects.filter(
        user=request.user,
        booking_date__gte=today
    ).order_by('booking_date')[:5] 
    
    # Count stats
    total_appointments = Booking.objects.filter(user=request.user).count()
    upcoming_count = appointments.count()
    
    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'upcoming_count': upcoming_count,
        'today': today,
        'show_navbar': True, 
    }
    return render(request, 'patient_dash.html', context)   

#------FOR VIEWING MY APPOINTMENTS----------------
@login_required
def my_appointments(request):
    appointments=Booking.objects.filter(user=request.user).order_by('-booking_date','-booking_time')
    return render(request,'my_app.html',{'appointments':appointments})
    

        

                                        #---- ADMIN/STAFF/DOCTOR VIEWS ----#


#------FOR ADMIN/STAFF/DOCTOR LOGIN----------------
def Admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if DoctorUser.objects.filter(user=user).exists():
                role=DoctorUser.objects.get(user=user)
                if role.is_staff:
                    return redirect("staff_dash")
                if role.doctor:
                    return redirect("doc_dash")
                messages.success(request, "Login successful!")
            else:
               return redirect("home")
        else:
            messages.error(request, "You entered wrong username or password")
    return render(request, "login.html")

#--------FOR DOCTOR DASHBOARD----------------
@login_required
def doctor_dashboard(request):
    role=DoctorUser.objects.get(user=request.user)
    appointments=Booking.objects.filter(doc_name=role.doctor)
    return render(request,'doctor_dash.html', {'appointments': appointments})


#-------FOR STAFF DASHBOARD----------------
@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return messages.error(request,"you are not authorized to view this page.")
    appointments=Booking.objects.all().order_by('-booking_date','-booking_time')
    
    return render(request,'staff_dash.html',{'appointments':appointments})


#------FOR APPROVING BOOKING STATUS----------------
@login_required
def status_approve(request,booking_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('staff_dash') 
    booking=get_object_or_404(Booking,id=booking_id)

    if request.method == 'POST':
        booking.status=True
        booking.save()
    return redirect('staff_dash')











    

def delete_booking(request,booking_id):
    if not request.user.is_staff:
        return messages.error(request,"you are not authorized to perform this action.")
    booking=Booking.objects.get(id=booking_id)
    booking.delete()
    return redirect('staff_dash')   










