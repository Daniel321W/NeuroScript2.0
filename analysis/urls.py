from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('add-patient-ajax/', views.add_patient_ajax, name='add_patient_ajax'),
    path('patients/<int:patient_id>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:patient_id>/delete/', views.patient_delete, name='patient_delete'),
    path('dodaj-badanie/', views.dodaj_badanie, name='dodaj_badanie'),
    path('historia/', views.historia_badan, name='historia_badan'),
    path('upload-badanie-ajax/', views.upload_badanie_ajax, name='upload_badanie_ajax'),
    path('cancel-badanie-ajax/', views.cancel_badanie_ajax, name='cancel_badanie_ajax'),
    path('save-raport-ajax/', views.save_raport_ajax, name='save_raport_ajax'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:report_id>/preview/', views.report_preview, name='report_preview'),
    path('reports/<int:report_id>/download/', views.report_download, name='report_download'),
]