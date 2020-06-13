from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class PatientForm(ModelForm):
	class Meta:
		model = Patient 
		fields = '__all__'
		exclude= ['user']

class DoctorForm(ModelForm):
	class Meta:
		model = Doctor
		fields = '__all__'
		exclude = ['user']


class AppointmentForm(ModelForm):
	class Meta:
		model = Appointment
		fields='__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password1','password2']

class PrescriptionForm(ModelForm):
	class Meta:
		model = Prescription
		fields='__all__'