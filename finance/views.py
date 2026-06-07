from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import Client

def welcome_page(request):
    return render(request, 'finance/welcome.html')
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        birthdate_str = request.POST.get('birthdate')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Client.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Пользователь с таким логином уже существует!'})
        if Client.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Этот Email уже зарегистрирован!'})
        try:
            birth_date = datetime.strptime(birthdate_str, '%d.%m.%Y').date()
        except ValueError:
            return render(request, 'register.html', {'error': 'Неверный формат даты. Используйте дд.мм.гггг'})
        hashed_password = make_password(password)
        Client.objects.create(
            full_name=full_name,
            email=email,
            birth_date=birth_date,
            username=username,
            password=hashed_password
        )
        return redirect('login')
    return render(request, 'register.html')