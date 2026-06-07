from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from datetime import datetime
from finance.models import Client
def welcome_page(request):
    return render(request, 'finance/welcome.html')
def register_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        birthdate_str = request.POST.get('birthdate')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Client.objects.filter(username=username).exists():
            return render(request, 'finance/register.html', {'error': 'Пользователь с таким логином уже существует!'})
        if Client.objects.filter(email=email).exists():
            return render(request, 'finance/register.html', {'error': 'Этот Email уже зарегистрирован!'})
        try:
            birth_date = datetime.strptime(birthdate_str, '%d.%m.%Y').date()
        except ValueError:
            return render(request, 'finance/register.html', {'error': 'Неверный формат даты. Используйте дд.мм.гггг'})
        hashed_password = make_password(password)
        Client.objects.create(
            full_name=full_name,
            email=email,
            birth_date=birth_date,
            username=username,
            password=hashed_password
        )
        return redirect('login')
    return render(request, 'finance/register.html')
def login_page(request):
    return render(request, 'finance/login.html')
def main_page(request):
    return render(request, 'finance/main.html')
def section_finances(request):
    return render(request, 'finance/section_finances.html')
def profile(request):
    return render(request, 'finance/profile.html')
def goals(request):
    return render(request, 'finance/my_goals.html')
def enter_exp(request):
    return render(request, 'finance/enter_expenses.html')
def finance_report(request):
    return render(request, 'finance/finance_report.html')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_page, name='welcome'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('main/', main_page, name='main'),
    path('section_finances/', section_finances, name='section_finances'),
    path('profile/', profile, name='profile'),
    path('my_goals/', goals, name='goals'),
    path('enter_expenses/', enter_exp, name='enter_expenses'),
    path('finance_report/', finance_report, name='finance_report'),
]