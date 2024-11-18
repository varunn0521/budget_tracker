from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, IncomeForm, ExpenseForm, EMIForm
from .models import Income, Expense, EMI, Category
from django.contrib.auth.forms import AuthenticationForm  
from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError  
from .forms import CustomUserCreationForm

def intro_page(request):
    return render(request, 'tracker/intro.html')

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, widget
    =forms.EmailInput(attrs={'class': 'form-control'}))


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in to continue.")  # Success message
            login(request, user)  # Log the user in after registration
            return redirect('dashboard')  # Redirect to the dashboard or login page
    else:
        form = RegisterForm()

    return render(request, 'tracker/register.html', {'form': form})


from django.contrib.auth import authenticate, login

def login_view(request):
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Specify the backend to use for authentication
            user = authenticate(request, username=email, password=password, backend='tracker.backend.EmailBackend')

            if user is not None:
                login(request, user)
                print("Login successful. Redirecting to dashboard.")  # Debugging
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid email or password")
                print("Authentication failed.")  # Debugging
        else:
            print("Form is invalid.")  # Debugging

    return render(request, 'tracker/login.html', {'form': form})



class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label="Password"
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise ValidationError("Invalid email or password")

        self.user_cache = user
        return self.cleaned_data


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')




@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully.')
            return redirect('dashboard')
    else:
        form = IncomeForm(user=request.user)

    return render(request, 'tracker/add_income.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('dashboard')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'tracker/add_expense.html', {'form': form})


@login_required
def add_emi_view(request):
    if request.method == 'POST':
        form = EMIForm(request.POST, user=request.user)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user
            emi.save()
            messages.success(request, 'EMI added successfully.')
            return redirect('dashboard')
    else:
        form = EMIForm(user=request.user)

    return render(request, 'tracker/add_emi.html', {'form': form})

@login_required
def view_incomes(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'tracker/view_incomes.html', {'incomes': incomes})

@login_required
def view_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'tracker/view_expenses.html', {'expenses': expenses})

@login_required
def dashboard(request):
    print(f"User authenticated: {request.user.is_authenticated}")  # Debugging
    print(f"Current user: {request.user}")  # Debugging
    # Fetch incomes, expenses, and emis
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    emis = EMI.objects.filter(user=request.user)

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
