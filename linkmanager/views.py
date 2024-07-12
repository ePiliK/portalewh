from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Link

@login_required
def dashboard(request):
    if request.user.is_staff:
        links = Link.objects.all()
    else:
        links = Link.objects.filter(client__user=request.user)
    return render(request, 'linkmanager/dashboard.html', {'links': links})