from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, IncomeForm, ExpenseForm
from .models import Income, Expense

# Register View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Add Income View
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'tracker/add_income.html', {'form': form})

# View Incomes
@login_required
def view_incomes(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'tracker/view_incomes.html', {'incomes': incomes})

# Add Expense View
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

# View Expenses
@login_required
def view_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'tracker/view_expenses.html', {'expenses': expenses})

# Dashboard View
@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')

# Home View (Redirect based on authentication status)
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')
