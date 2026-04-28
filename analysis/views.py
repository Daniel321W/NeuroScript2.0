from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from db_models.models import Pacjent

@login_required
@never_cache
def dashboard(request):
    patients = Pacjent.objects.filter(lekarz=request.user)
    
    context = {
        'username': request.user.username,
        'patients': patients,
    }
    return render(request, 'analysis/dashboard.html', context)

@login_required
def add_patient_ajax(request):
    if request.method == "POST":
        rok = request.POST.get('rok_urodzenia')
        plec = request.POST.get('plec')
        
        if rok and plec:
            pacjent = Pacjent.objects.create(
                rok_urodzenia=rok,
                plec=plec,
                lekarz=request.user
            )
            return JsonResponse({
                "success": True, 
                "id": pacjent.id, 
                "identyfikator": pacjent.identyfikator_pacjenta
            })
            
    return JsonResponse({"success": False, "error": "Niepoprawne dane"})

@login_required
def patient_list(request):
    search_query = request.GET.get('search', '').strip()
    patients = Pacjent.objects.filter(lekarz=request.user)
    
    if search_query:
        if search_query.isdigit():
            patients = patients.filter(
                Q(identyfikator_pacjenta__icontains=search_query) | 
                Q(rok_urodzenia=int(search_query))
            )
        else:
            patients = patients.filter(identyfikator_pacjenta__icontains=search_query)
            
    return render(request, 'analysis/patient_list.html', {
        'patients': patients,
        'search_query': search_query
    })

@login_required
def patient_edit(request, patient_id):
    pacjent = get_object_or_404(Pacjent, id=patient_id, lekarz=request.user)
    
    if request.method == 'POST':
        pacjent.rok_urodzenia = request.POST.get('rok_urodzenia')
        pacjent.plec = request.POST.get('plec')
        pacjent.save()
        
    return redirect('patient_list')

@login_required
def patient_delete(request, patient_id):
    pacjent = get_object_or_404(Pacjent, id=patient_id, lekarz=request.user)
    
    if request.method == 'POST':
        pacjent.delete()
        
    return redirect('patient_list')