from django.shortcuts import render

def login_view(request):
    return render(request, 'users/login.html', context = {})

def register_view(request):
    return render(request, 'users/register.html', context = {})

def contact_view(request):
    return render(request, 'users/contacto.html', context = {})