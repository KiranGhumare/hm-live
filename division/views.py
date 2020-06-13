from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import PatientForm, AppointmentForm, CreateUserForm,PrescriptionForm, DoctorForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only

def home(request):
	return render(request, 'division/index.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['human_resource'])
def human_resource(request):
	return render(request, 'division/human_resource.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['human_resource'])
def dashboard_hr(request):
	pats= Patient.objects.all()
	total_patients = pats.count()
	docs = Doctor.objects.all()
	doc_count=docs.count()
	active = docs.filter(status='Active').count()
	context = {'docs':docs,'doc_count':doc_count,
	'total_patients':total_patients,'active':active}
	return render(request, 'division/hr_dash.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Receptionist'])
def dashboard(request):
	appointments = Appointment.objects.all()
	total_appoints = appointments.count()
	completed = appointments.filter(status='Completed').count()
	pending = appointments.filter(status='Pending').count()
	pats= Patient.objects.all()

	context = {'appointments':appointments, 
	'total_appoints':total_appoints,'completed':completed,
	'pending':pending,'pats':pats}
	return render(request, 'division/dashboard.html',context)


def CreatePatient(request):
	form = PatientForm()
	if request.method=='POST':
		form= PatientForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/reception')
	context={'form':form}
	return render(request, 'division/patient_form.html',context)

def CreateAppoint(request):
	form = AppointmentForm()
	if request.method=='POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/reception')
	context={'form':form}
	return render(request, 'division/appoint_form.html', context)
@unauthenticated_user
def register(request):
	
	form= CreateUserForm()
	if request.method=='POST':
		form= CreateUserForm(request.POST)
		if form.is_valid():
			ty=request.POST.getlist('check')
			print(ty)
			user= form.save()
			if(ty[0]=='Patient'):
				Patient.objects.create(user=user,)
				group = Group.objects.get(name='Patient')
				user.groups.add(group)
			else:
				Doctor.objects.create(user=user,)
				group = Group.objects.get(name='Doctor')
				user.groups.add(group)
			username=form.cleaned_data.get('username')
			
			
			messages.success(request, 'Account was created for ' + username)


			return redirect('login')
	context={'form':form}
	return render(request, 'division/register.html',context)
@unauthenticated_user
def loginpage(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user= authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			if request.user.groups.exists():
				group= request.user.groups.all()[0].name
			if group == 'Patient':
				return redirect('pat')
			if group=='Doctor':
				return redirect('doc')
			if group=='Receptionist':
				return redirect('reception')
			if group=='human_resource':
				return redirect('human_resource')
			if group=='admin':
				return redirect('#')
			
		else:
			messages.info(request,'Username OR password is incorrect')
	return render(request, 'division/login.html')


def logoutUser(request):
	logout(request)
	return redirect('home')
@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def PatientPage(request):
	return render(request, 'division/patient.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def DoctorPage(request):
	return render(request, 'division/doctor.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def Presci(request):
	pres=request.user.doctor.prescription_set.all()
	print(pres)  
	context={'pres':pres}
	return render(request, 'division/prescription.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def CreatePresci(request):
	form = PrescriptionForm()
	if request.method=='POST':
		form = PrescriptionForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/prescription')
	context={'form':form}
	return render(request, 'division/prescription_form.html', context)


	


@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def appointments(request):
	appoints=request.user.patient.appointment_set.all()
	print(appoints)  
	context={'appoints':appoints}
	return render(request, 'division/appointments.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def app_doc(request):
	appoints=request.user.doctor.appointment_set.all()
	print(appoints)  
	context={'appoints':appoints}
	return render(request, 'division/appoint_doctor.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def med_history(request):
	pres=request.user.patient.prescription_set.all()
	print(pres)  
	context={'pres':pres}
	return render(request, 'division/medical_history.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['Receptionist'])
def reception(request):
	return render(request, 'division/reception.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def profile_patient(request):
	patient = request.user.patient
	form = PatientForm(instance=patient)

	if request.method == 'POST':
		form = PatientForm(request.POST, request.FILES,instance=patient)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'division/profile_patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def profile_doctor(request):
	doctor = request.user.doctor
	form = DoctorForm(instance=doctor)

	if request.method == 'POST':
		form = DoctorForm(request.POST, request.FILES,instance=doctor)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'division/profile_doctor.html', context)

def about(request):
	return render(request, 'division/about.html')
@login_required(login_url='login')

def update_patient(request,pk):
	pat= Patient.objects.get(id=pk)
	form=PatientForm(instance=pat)
	if request.method=='POST':
		form =PatientForm(request.POST, instance=pat)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')
	context={'form':form}
	return render(request, 'division/patient_form.html',context)

def delete_patient(request, pk):
	pat = Patient.objects.get(id=pk)
	if request.method == "POST":
		pat.delete()
		return redirect('/dashboard')

	context = {'item':pat}
	return render(request, 'division/delete.html', context)

def update_appoint(request,pk):
	appoint= Appointment.objects.get(id=pk)
	form=AppointmentForm(instance=appoint)
	if request.method=='POST':
		form =AppointmentForm(request.POST, instance=appoint)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')
	context={'form':form}
	return render(request, 'division/appoint_form.html',context)

def delete_appoint(request, pk):
	appoint = Appointment.objects.get(id=pk)
	if request.method == "POST":
		appoint.delete()
		return redirect('/dashboard')

	context = {'item':appoint}
	return render(request, 'division/delete.html', context)

def update_doctor(request,pk):
	doc= Doctor.objects.get(id=pk)
	form=DoctorForm(instance=doc)
	if request.method=='POST':
		form =DoctorForm(request.POST, instance=doc)
		if form.is_valid():
			form.save()
			return redirect('/dash_hr')
	context={'form':form}
	return render(request, 'division/doctor_form.html',context)

def delete_doctor(request, pk):
	doc = Doctor.objects.get(id=pk)
	if request.method == "POST":
		doc.delete()
		return redirect('/dash_hr')

	context = {'item':doc}
	return render(request, 'division/delete_doc.html', context)

def contact(request):
	return render(request, 'division/contact.html')

def complaint(request):
	if request.method=="POST":
		name=request.POST.get('name', '')
		phone=request.POST.get('phone', '')
		email=request.POST.get('email', '')
		desc=request.POST.get('desc', '')

		contact=Contact(name=name, phone=phone, email=email, desc=desc)
		contact.save()
		return redirect('/home')

	return render(request, "division/contact.html")
	

