from django.db import models
from django.contrib.auth.models import User

class Departments(models.Model):
    dep_name=models.CharField(max_length=250)
    dep_description=models.TextField(max_length=300,null=True)

    def __str__(self):
        return self.dep_name
    
class Doctors(models.Model):
    doc_name=models.CharField(max_length=250)
    doc_spec=models.CharField(max_length=250)
    doc_dept=models.ForeignKey(Departments,on_delete=models.CASCADE)
    doc_image=models.ImageField(upload_to='doctors/')
    start_time=models.TimeField(default="09:00")
    end_time=models.TimeField(default="21:00")

    def __str__(self):
        return 'DR.' + self.doc_name + '-('+self.doc_spec+')'
    
class DoctorUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_staff=models.BooleanField(default=False)
    doctor=models.ForeignKey(Doctors,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.user.username
    
class UserProfile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    address=models.TextField(max_length=300)
    def __str__(self):
        return self.user.username
    


class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    patient_name=models.CharField(max_length=250,null=True,blank=True)
    date_of_birth=models.DateField(null=True)
    dep_name=models.ForeignKey(Departments,on_delete=models.CASCADE)
    doc_name=models.ForeignKey(Doctors,on_delete=models.CASCADE)
    booking_date=models.DateField()
    booked_on=models.DateField(auto_now=True)
    booking_time=models.TimeField(auto_now_add=True)
    appointment_time=models.TimeField(null=True)
    status=models.BooleanField(default=False)
    

    def __str__(self):
        return self.user +"- booked  Dr. "+ self.doc_name.doc_name +  " on " +str(self.booking_date)
    

    

    
    
