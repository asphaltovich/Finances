from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from datetime import datetime
from .models import Client, Wallet, Expense, Income, Goal
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
    if 'client_id' in request.session:
        return redirect('main')
    if request.method == 'POST':
        login_data = request.POST.get('login')
        password_data = request.POST.get('password')
        try:
            client = Client.objects.get(username=login_data)
        except Client.DoesNotExist:
            return render(request, 'finance/login.html', {'error': 'Пользователь с таким логином не зарегистрирован!'})
        if check_password(password_data, client.password):
            request.session['client_id'] = client.id
            request.session['client_username'] = client.username
            return redirect('main')
        else:
            return render(request, 'finance/login.html', {'error': 'Неверный пароль!'})
    return render(request, 'finance/login.html')
def logout_user(request):
    request.session.flush()
    return redirect('welcome')
def main_page(request):
    if 'client_id' not in request.session:
        return redirect('login')
    return render(request, 'finance/main.html')
def section_finances(request):
    if 'client_id' not in request.session:
        return redirect('login')
    return render(request, 'finance/section_finances.html')
def profile(request):
    if 'client_id' not in request.session:
        return redirect('login')
    client = Client.objects.get(id=request.session['client_id'])
    return render(request, 'finance/profile.html', {'client': client})
def goals(request):
    if 'client_id' not in request.session:
        return redirect('login')
    return render(request, 'finance/my_goals.html')
def enter_exp(request):
    if 'client_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        wallet_name = request.POST.get('wallet_type')
        category_name = request.POST.get('category')
        amount_val = request.POST.get('amount')
        client = Client.objects.get(id=request.session['client_id'])
        wallet, created = Wallet.objects.get_or_create(
            name=wallet_name,
            client=client
        )
        Expense.objects.create(
            client=client,
            wallet=wallet,
            category=category_name,
            amount=amount_val
        )
        return redirect('enter_exp')
    return render(request, 'finance/enter_expenses.html')
def enter_inc(request):
    if 'client_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        wallet_name = request.POST.get('wallet_type')
        category_name = request.POST.get('category')
        amount_val = request.POST.get('amount')
        client = Client.objects.get(id=request.session['client_id'])
        wallet, created = Wallet.objects.get_or_create(
            name=wallet_name,
            client=client
        )
        Income.objects.create(
            client=client,
            wallet=wallet,
            category=category_name,
            amount=amount_val
        )
        return redirect('enter_incomes')
    return render(request, 'finance/enter_incomes.html')
def add_goal(request):
    if 'client_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        name_val = request.POST.get('name')
        desc_val = request.POST.get('description')
        amount_val = request.POST.get('amount')
        client = Client.objects.get(id=request.session['client_id'])
        Goal.objects.create(
            client=client,
            name=name_val,
            description=desc_val,
            amount=amount_val
        )
        return redirect('goals')
    return render(request, 'finance/add_goal.html')
def finance_report(request):
    if 'client_id' not in request.session:
        return redirect('login')
    client_id = request.session['client_id']
    expenses = Expense.objects.filter(client_id=client_id).order_by('-id')
    incomes = Income.objects.filter(client_id=client_id).order_by('-id')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    context = {
        'expenses': expenses,
        'incomes': incomes,
        'total_expense': total_expense,
        'total_income': total_income,
    }
    return render(request, 'finance/finance_report.html', context)