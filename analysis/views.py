from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def dashboard(request):
    return render(request, 'analysis/dashboard.html', {'username': request.user.username})