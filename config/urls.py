from django.contrib import admin
from django.urls import path
from finance import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome_page, name='welcome'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),  # НОВЫЙ ПУТЬ ДЛЯ ВЫХОДА
    path('main/', views.main_page, name='main'),
    path('section_finances/', views.section_finances, name='section_finances'),
    path('profile/', views.profile, name='profile'),
    path('my_goals/', views.goals, name='goals'),
    path('enter_expenses/', views.enter_exp, name='enter_expenses'),
    path('finance_report/', views.finance_report, name='finance_report'),
    path('enter_incomes/', views.enter_inc, name='enter_incomes'),
]