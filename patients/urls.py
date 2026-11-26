
from django.contrib import admin
from django.urls import path
from patients import views

urlpatterns = [
    path('patientregister', views.PatientListCreate.as_view()),
    path('view_appointment', views.ViewAppointment.as_view()),
    path('search_patients', views.PatientSearch.as_view()),
    path('update_appointment/<int:pk>', views.PatientUpdateAppointment.as_view()),
    path('delete_patient/<int:pk>', views.PatientDelete.as_view()),
    path('department_summary', views.DepartmentSummary.as_view()),
]
