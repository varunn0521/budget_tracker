from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page, redirects based on authentication
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('add_income/', views.add_income, name='add_income'),  # Add Income page
    path('view_incomes/', views.view_incomes, name='view_incomes'),  # View Incomes page
    path('add_expense/', views.add_expense, name='add_expense'),  # Add Expense page
    path('view_expenses/', views.view_expenses, name='view_expenses'),  # View Expenses page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page
]
