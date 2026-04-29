from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('add-patient-ajax/', views.add_patient_ajax, name='add_patient_ajax'),
    path('patients/<int:patient_id>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:patient_id>/delete/', views.patient_delete, name='patient_delete'),
    path('dodaj-badanie/', views.dodaj_badanie, name='dodaj_badanie'),
    path('historia/', views.historia_badan, name='historia_badan'),
]