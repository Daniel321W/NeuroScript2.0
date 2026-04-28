from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from db_models.models import Pacjent

@login_required
def patient_list(request):
    search_query = request.GET.get('search', '')
    
    patients = Pacjent.objects.filter(lekarz=request.user)
    
    if search_query:
        patients = patients.filter(
            identyfikator_pacjenta__icontains=search_query
        ) | patients.filter(
            rok_urodzenia__icontains=search_query
        )
        
    return render(request, 'analysis/patient_list.html', {'patients': patients})