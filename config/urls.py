from django.contrib import admin
from django.urls import path
from django.shortcuts import render
def welcome_page(request):
    return render(request, 'finance/welcome.html')
def register_page(request):
    return render(request, 'finance/register.html')
def login_page(request):
    return render(request, 'finance/login.html')
def main_page(request):
    return render(request, 'finance/main.html')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_page, name='welcome'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('main/', main_page, name='main'),
]
