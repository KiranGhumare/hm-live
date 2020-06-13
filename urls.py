from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns= [
	path('',views.home, name="home"),
	# path('patient/<str:pk_test>/', views.patient, name="patient"),

	path('dashboard/',views.dashboard, name="dashboard"),
	path('appointments/', views.appointments, name="appointment"),
	path('createPatient/', views.CreatePatient, name="createPatient"),
	path('createAppointment/', views.CreateAppoint, name="createAppointment"),
	path('register/', views.register, name="register" ),
	path('login/',views.loginpage, name="login"),
	path('logout/',views.logoutUser, name="logout"),
	path('pat/',views.PatientPage, name="pat"),
	path('doc/',views.DoctorPage, name="doc"),
	path('prescription/',views.Presci, name="prescription"),
	path('presci/', views.CreatePresci, name="presci"),
	path('app_doc/',views.app_doc, name="app_doc"),
	path('medical_history/', views.med_history, name="medical_history"),
	path('reception/', views.reception, name="reception"),
	path('profile_patient/', views.profile_patient, name="profile_patient"),
	path('profile_doctor/', views.profile_doctor, name="profile_doctor"),
	path('about/', views.about, name="about"),
	path('human_resource/', views.human_resource, name="human_resource"),
	path('dash_hr/', views.dashboard_hr, name="dash_hr"),
	path('update_patient/<str:pk>/', views.update_patient, name="update_patient"),
	path('delete_patient/<str:pk>/', views.delete_patient, name="delete_patient"),
	path('update_appoint/<str:pk>/', views.update_appoint, name="update_appoint"),
	path('delete_appoint/<str:pk>/', views.delete_appoint, name="delete_appoint"),
	path('update_doctor/<str:pk>/', views.update_doctor, name="update_doctor"),
	path('delete_doctor/<str:pk>/', views.delete_doctor, name="delete_doctor"),
	path('contact/', views.complaint, name="contact"),
	
	
]