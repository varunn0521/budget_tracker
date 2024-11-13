from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, IncomeForm, ExpenseForm, EMIForm  # Add EMIForm here
from .models import Income, Expense, EMI  # Add EMI model here

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

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Associate the income with the logged-in user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'tracker/add_income.html', {'form': form})

@login_required
def view_incomes(request):
    incomes = Income.objects.filter(user=request.user)  # Filter by the logged-in user
    return render(request, 'tracker/view_incomes.html', {'incomes': incomes})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate the expense with the logged-in user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

@login_required
def view_expenses(request):
    expenses = Expense.objects.filter(user=request.user)  # Filter by the logged-in user
    return render(request, 'tracker/view_expenses.html', {'expenses': expenses})

@login_required
def dashboard(request):
    # Fetch incomes, expenses, and emis associated with the logged-in user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    emis = EMI.objects.filter(user=request.user)  # Make sure EMI model is associated with the user

    # Calculate total income, total expenses, and balance
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    balance = total_income - total_expenses

    # Prepare context data
    context = {
        'incomes': incomes,
        'expenses': expenses,
        'emis': emis,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
    }
    
    return render(request, 'tracker/dashboard.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

@login_required
def add_emi(request):
    if request.method == 'POST':
        form = EMIForm(request.POST)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user  # Associate the EMI with the logged-in user
            emi.save()
            return redirect('dashboard')
    else:
        form = EMIForm()
    return render(request, 'tracker/add_emi.html', {'form': form})
