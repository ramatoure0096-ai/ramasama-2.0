from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def log_in(request):
    if request.method == 'POST':
        f = AuthenticationForm(data=request.POST)
        if f.is_valid():
            u = f.get_user()
            login(request, u)
            messages.success(request, "Bienvenue !")
            return redirect('login')
    else:
        f = AuthenticationForm()
    return render(request, 'ramasama/login.html', {'form': f}) 

def log_out(request):
    logout(request)
    messages.info(request, "Bye !")
    return redirect('login')
# Create your views here.
