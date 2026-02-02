from urllib import request
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Doctors,DoctorUser,Departments,Booking
from .forms import *
from django.contrib import messages

# Create your views here.
def about(request):
    return render(request,'about.html')



def login_view(request):
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
            return redirect("homepage")
        else:
            messages.error(request, "You entered wrong username or password")
    return render(request, "login.html")


@login_required
def doctor_dashboard(request):
    role=DoctorUser.objects.get(user=request.user)
    appointments=Booking.objects.filter(doc_name=role.doctor)
    return render(request,'doctor_dash.html', {'appointments': appointments})



@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return messages.error(request,"you are not authorized to view this page.")
    appointments=Booking.objects.all().order_by('-booking_date','-booking_time')
    
    return render(request,'staff_dash.html',{'appointments':appointments})



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


def book_appointment(request):
    if request.method=='POST':
        form=BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'appointment.html')
        else:
            messages.error(request,"Invalid Input Data")
    else:
        form = BookingForm(request.GET) if request.GET else BookingForm()
    context = {'form': form}
    return render(request,'booking.html',context)
    
    

def delete_booking(request,booking_id):
    if not request.user.is_staff:
        return messages.error(request,"you are not authorized to perform this action.")
    booking=Booking.objects.get(id=booking_id)
    booking.delete()
    return redirect('staff_dash')   




def logout_page(request):
    logout(request)
    return render(request,'home.html')




def contact(request):
    return render(request,'contact.html')

    



