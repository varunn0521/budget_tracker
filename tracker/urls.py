from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro_page, name='intro'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_income/', views.add_income, name='add_income'),
    path('view_incomes/', views.view_incomes, name='view_incomes'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_emi/', views.add_emi_view, name='add_emi'),  
]
