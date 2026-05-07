from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from db_models.models import Pacjent, Badanie, WynikAnalizyAI, RaportKoncowy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from analysis.ml.services.predict import predict

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('/admin/')
            else:
                return render(request, 'registration/admin_login.html', {
                    'form': form,
                    'error': 'To konto nie ma uprawnień administratora.'
                })
    else:
        form = AuthenticationForm()
    return render(request, 'registration/admin_login.html', {'form': form})

@login_required
@never_cache
def dashboard(request):
    patients = Pacjent.objects.filter(lekarz=request.user)
    return render(request, 'analysis/dashboard.html', {'patients': patients})

@login_required
def upload_badanie_ajax(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        plik_badania = request.FILES.get('badanie_plik')
        
        if patient_id and plik_badania:
            pacjent = get_object_or_404(Pacjent, id=patient_id, lekarz=request.user)
            
            fs = FileSystemStorage()
            nazwa_zapisana = fs.save(plik_badania.name, plik_badania)
            sciezka_url = fs.url(nazwa_zapisana)
            
            badanie = Badanie.objects.create(pacjent=pacjent, sciezka_do_pliku=sciezka_url)
            
            try:
                plik_badania.seek(0)
                file_bytes = plik_badania.read()
                wynik_ai = predict(file_bytes)
                prawdziwy_wynik = round(wynik_ai["probability"] * 100, 2)
                
            except Exception as e:
                badanie.delete()
                return JsonResponse({'success': False, 'error': f'Błąd analizy AI: {str(e)}'})
            
            return JsonResponse({
                'success': True,
                'badanie_id': badanie.id,
                'image_url': sciezka_url,
                'ai_prob': prawdziwy_wynik
            })
            
    return JsonResponse({'success': False, 'error': 'Brak danych lub pliku'})

@login_required
def save_raport_ajax(request):
    if request.method == 'POST':
        badanie_id = request.POST.get('badanie_id')
        ai_prob = request.POST.get('ai_prob')
        notatki = request.POST.get('notatki', '')
        
        badanie = get_object_or_404(Badanie, id=badanie_id, pacjent__lekarz=request.user)
        
        wynik = WynikAnalizyAI.objects.create(badanie=badanie, prawdopodobienstwo_choroby=float(ai_prob))
        raport = RaportKoncowy.objects.create(wynik=wynik, notatki_lekarza=notatki)
        
        return JsonResponse({'success': True, 'raport_id': raport.id})
    return JsonResponse({'success': False})

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
def historia_badan(request):
    search_query = request.GET.get('search', '').strip()
    
    badania = Badanie.objects.filter(pacjent__lekarz=request.user)

    if search_query:
        filters = Q(pacjent__identyfikator_pacjenta__icontains=search_query)

        if search_query.isdigit():
            filters |= Q(id=search_query)

        if len(search_query) == 4 and search_query.isdigit():
            filters |= Q(data_wgrania__year=search_query)
        else:
            filters |= Q(data_wgrania__icontains=search_query)

        badania = badania.filter(filters)

    badania = badania.order_by('-data_wgrania')

    context = {
        'badania': badania,
        'search_query': search_query,
    }
    
    return render(request, 'analysis/historia_badan.html', context)

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

@login_required
def dodaj_badanie(request):
    if request.method == 'POST':
        pacjent_id = request.POST.get('patient_id')
        plik = request.FILES.get('handwriting_image')
        
        if not pacjent_id or not plik:
            messages.error(request, 'Błąd: Wybierz pacjenta z listy i dodaj zdjęcie próbki.')
            return redirect('dashboard')
            
        pacjent = get_object_or_404(Pacjent, id=pacjent_id, lekarz=request.user)
        
        if not plik.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            messages.error(request, 'Błąd: Dozwolone są tylko pliki graficzne JPG i PNG.')
            return redirect('dashboard')
            
        fs = FileSystemStorage()
        nazwa_pliku = fs.save(f'badania/{plik.name}', plik)
        sciezka_url = fs.url(nazwa_pliku)
        
        Badanie.objects.create(
            pacjent=pacjent,
            sciezka_do_pliku=sciezka_url
        )
        
        messages.success(request, f'Pomyślnie wgrano próbkę dla pacjenta {pacjent.identyfikator_pacjenta}!')
        return redirect('dashboard')

    return redirect('dashboard')

@login_required
def cancel_badanie_ajax(request):
    if request.method == 'POST':
        badanie_id = request.POST.get('badanie_id')
        if badanie_id:
            badanie = get_object_or_404(Badanie, id=badanie_id, pacjent__lekarz=request.user)
            badanie.delete()
            return JsonResponse({'success': True})
            
    return JsonResponse({'success': False})

@login_required
def report_list(request):
    search_query = request.GET.get('search', '').strip()
    
    reports = RaportKoncowy.objects.filter(
        wynik__badanie__pacjent__lekarz=request.user
    ).order_by('-data_utworzenia')

    if search_query:
        if search_query.isdigit():
            reports = reports.filter(
                Q(id=search_query) | 
                Q(wynik__badanie__pacjent__identyfikator_pacjenta__iexact=search_query)
            )
        else:
            reports = reports.filter(
                wynik__badanie__pacjent__identyfikator_pacjenta__icontains=search_query
            )

    return render(request, 'analysis/reports.html', {
        'reports': reports,
        'search_query': search_query,
    })

def generate_pdf(request, report_id, as_attachment=False):
    """Pomocnicza funkcja generująca PDF w locie"""
    raport = get_object_or_404(RaportKoncowy, id=report_id, wynik__badanie__pacjent__lekarz=request.user)
    
    html_string = render_to_string('analysis/pdf_report.html', {'raport': raport}, request=request)
    
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    nazwa_pliku = f"Report_{raport.wynik.badanie.pacjent.identyfikator_pacjenta}_{raport.data_utworzenia.strftime('%Y%m%d')}.pdf"
    
    if as_attachment:
        response['Content-Disposition'] = f'attachment; filename="{nazwa_pliku}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{nazwa_pliku}"'
        
    return response

@login_required
def report_preview(request, report_id):
    return generate_pdf(request, report_id, as_attachment=False)

@login_required
def report_download(request, report_id):
    return generate_pdf(request, report_id, as_attachment=True)