from django import forms
from.models import Booking,Doctors
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15,required=True)
    class Meta:
        model = User
        fields = ['username','email','phone','password1']

class Date_Input(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    appointment_time= forms.ChoiceField(choices=[])
    class Meta:
       model=Booking
       fields = ['patient_name','date_of_birth','dep_name','doc_name','booking_date','appointment_time']

       widgets = {
           'booking_date': Date_Input(),
           'appointment_time' : forms.Select(),
           'patient_name': forms.TextInput(attrs={'placeholder': 'Enter patient full name'}),
            'date_of_birth': Date_Input(),
       }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_date = self.data.get('booking_date')
        selected_doctor = self.data.get('doc_name')
        self.fields['appointment_time'].choices = self.get_time_slot(selected_date, selected_doctor)

    def get_time_slot(self, selected_date, selected_doctor=None):
        # Show time slots only when both doctor and date are selected (slots are per doctor)
        if not selected_date or not selected_doctor:
            return [('', '— Select doctor and date first —')]

        # Only consider bookings for this doctor on this date
        booked_times = list(
            Booking.objects.filter(
                booking_date=selected_date,
                doc_name_id=selected_doctor
            ).values_list('appointment_time', flat=True)
        )
        booked_times = [t.strftime('%H:%M') for t in booked_times if t]

        times = []
        hour = 9
        while hour <= 17:
            for minutes in ['00', '30']:
                if hour == 17 and minutes == '30':
                    break

                time_value = f"{hour:02d}:{minutes}"
                if time_value in booked_times:
                    continue

                display_hour = hour
                period = "AM"
                if hour == 12:
                    period = "PM"
                elif hour > 12:
                    display_hour = hour - 12
                    period = "PM"
                time_label = f"{display_hour:02d}:{minutes} {period}"
                times.append((time_value, time_label))

            hour += 1

        if not times:
            return [('', 'No slots available for this doctor on this date')]
        return times
