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
from .tasks import process_emis  # Correct import for process_emis task
from django.http import HttpResponse, JsonResponse
import json
from .models import Category
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def intro_page(request):
    return render(request, 'tracker/intro.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in to continue.")
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'tracker/register.html', {'form': form})

def login_view(request):
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate the user using custom backend
            user = authenticate(request, username=email, password=password, backend='tracker.backend.EmailBackend')

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid email or password")
        else:
            print("Form is invalid.")

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
    # Fetch income categories for the current user
    categories = Category.objects.filter(user=request.user, type='income')

    if request.method == 'POST':
        # Retrieve data from the POST request
        amount = request.POST.get('amount')
        category_name = request.POST.get('category_name')  # Adding support for a new category name
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        # Check if the required fields are provided
        if not amount or not category_id:
            return JsonResponse({'success': False, 'message': 'Amount and category are required fields.'}, status=400)

        # Try to get the category, if not found, create a new one
        try:
            if category_id == 'new':  # User wants to add a new category
                if not category_name:
                    return JsonResponse({'success': False, 'message': 'Category name is required to create a new category.'}, status=400)

                # Create the new category
                category = Category.objects.create(
                    name=category_name,
                    user=request.user,
                    type='income'  # Ensure the category is for income
                )
            else:
                # Get the category object based on the provided category ID
                category = Category.objects.get(id=category_id, user=request.user)  # Ensure category belongs to the current user

            # Set the current date if not provided
            date = timezone.now()

            # Create and save the income entry
            income = Income.objects.create(
                amount=amount,
                category=category,
                description=description,
                user=request.user,  # Associate the income entry with the current user
                date=date  # Ensure the date is set
            )

            # Return success response for AJAX request
            return JsonResponse({'success': True, 'message': 'Income added successfully!', 'id': income.id})

        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Failed to find the specified category.'}, status=400)

        except Exception as e:
            # If something goes wrong, return an error response
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

    # For GET requests, render the form to add income
    return render(request, 'tracker/add_income.html', {'categories': categories})
        
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Expense
from django.contrib.auth.decorators import login_required

@login_required
def add_expense(request):
    # Fetch expense categories for the current user
    categories = Category.objects.filter(user=request.user, type='expense')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category_name = request.POST.get('category_name')  # Adding support for a new category name
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        # Check if the required fields are provided
        if not amount or not category_id:
            return JsonResponse({'success': False, 'message': 'Amount and category are required fields.'}, status=400)

        # Try to get the category, if not found, create a new one
        try:
            if category_id == 'new':  # User wants to add a new category
                if not category_name:
                    return JsonResponse({'success': False, 'message': 'Category name is required to create a new category.'}, status=400)

                # Create the new category
                category = Category.objects.create(
                    name=category_name,
                    user=request.user,
                    type='expense'  # Ensure the category is for expense
                )
            else:
                # Get the category object based on the provided category ID
                category = Category.objects.get(id=category_id, user=request.user)  # Ensure category belongs to the current user

            # Set the current date if not provided
            date = timezone.now()

            # Create and save the expense entry
            expense = Expense.objects.create(
                amount=amount,
                category=category,
                description=description,
                user=request.user,  # Associate the expense entry with the current user
                date=date  # Ensure the date is set
            )

            # Return success response for AJAX request
            return JsonResponse({'success': True, 'message': 'Expense added successfully!', 'id': expense.id})

        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Failed to find the specified category.'}, status=400)

        except Exception as e:
            # If something goes wrong, return an error response
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

    # For GET requests, render the form to add expense
    return render(request, 'tracker/add_expense.html', {'categories': categories})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import EMIForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import EMI

@login_required
def add_emi_view(request):
    if request.method == 'POST':
        # Collect the form data
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        frequency = request.POST.get('frequency')  # EMI frequency (e.g., monthly, yearly)
        remaining_installments = request.POST.get('remaining_installments')  # Remaining installments
        category_id = request.POST.get('category')  # Optional: If you want to handle categories for EMI

        # Validate required fields
        if not amount or not frequency or not remaining_installments:
            return JsonResponse({'success': False, 'message': 'Amount, frequency, and installments are required fields.'}, status=400)

        try:
            # If a category is provided, fetch it; otherwise, skip
            category = None
            if category_id and category_id != 'new':  # Assuming 'new' means creating a new category
                category = Category.objects.get(id=category_id, user=request.user)  # Ensure the category belongs to the current user

            # Create and save the EMI entry
            emi = EMI.objects.create(
                amount=amount,
                description=description,
                frequency=frequency,
                remaining_installments=remaining_installments,
                user=request.user,  # Associate the EMI entry with the current user
                category=category,  # Optionally associate a category
            )

            # Return success response for AJAX request
            return JsonResponse({'success': True, 'message': 'EMI added successfully!', 'id': emi.id})

        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Failed to find the specified category.'}, status=400)

        except Exception as e:
            # If something goes wrong, return an error response
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

    # For GET requests, render the form to add EMI
    return render(request, 'tracker/add_emi.html')


@login_required
def view_incomes(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'tracker/view_incomes.html', {'incomes': incomes})


@login_required
def view_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'tracker/view_expenses.html', {'expenses': expenses})


from django.shortcuts import render
from django.db.models import Sum
from .models import Income, Expense, EMI

from django.db.models import Sum

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Income, Expense, EMI

@login_required
def dashboard(request):
    # Fetch incomes, expenses, and emis for the logged-in user including category and description
    incomes = Income.objects.filter(user=request.user).select_related('category').values('amount', 'date', 'category__name', 'description')[:6]
    expenses = Expense.objects.filter(user=request.user).select_related('category').values('amount', 'date', 'category__name', 'description')[:6]
    emis = EMI.objects.filter(user=request.user).values('amount', 'due_date', 'description', 'start_date', 'next_payment_date')[:6]

    # Calculate total income, total expenses, and balance using aggregate
    total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    # Prepare context data to be passed to the template
    context = {
        'incomes': list(incomes),
        'expenses': list(expenses),
        'emis': list(emis),
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

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category  # Ensure to import the correct model

@csrf_exempt  # Exempt CSRF for testing; remove it when using CSRF tokens in production
def add_category(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Try parsing JSON data from the frontend
            category_name = data.get('name')
            category_type = data.get('type')

            if not category_name or not category_type:
                return JsonResponse({'success': False, 'message': 'Category name and type are required'})

            # Ensure no duplicate category is created for the same user
            category, created = Category.objects.get_or_create(
                name=category_name,
                type=category_type,
                user=request.user  # Assuming `request.user` is the logged-in user
            )

            if created:
                return JsonResponse({
                    'success': True,
                    'category_id': category.id,
                    'name': category.name,
                    'type': category.type
                })
            else:
                return JsonResponse({'success': False, 'message': 'Category already exists'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data. Please check your request body.'})

        except Exception as e:
            # Log the error
            print(f"Error in adding category: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method. POST required.'})


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Income, Category
from django.contrib.auth.decorators import login_required

@login_required
def edit_income(request, income_id):
    # Fetch income entry to edit and ensure it belongs to the logged-in user
    income = get_object_or_404(Income, id=income_id, user=request.user)

    # Fetch income categories for the current user
    categories = Category.objects.filter(user=request.user, type='income')

    if request.method == 'POST':
        # Retrieve data from the POST request
        amount = request.POST.get('amount')
        category_name = request.POST.get('category_name')  # Adding support for a new category name
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        # Check if the required fields are provided
        if not amount or not category_id:
            return JsonResponse({'success': False, 'message': 'Amount and category are required fields.'}, status=400)

        try:
            # Handle new category creation or retrieve the existing category
            if category_id == 'new':  # User wants to add a new category
                if not category_name:
                    return JsonResponse({'success': False, 'message': 'Category name is required to create a new category.'}, status=400)

                # Create the new category
                category = Category.objects.create(
                    name=category_name,
                    user=request.user,
                    type='income'  # Ensure the category is for income
                )
            else:
                # Get the existing category
                category = get_object_or_404(Category, id=category_id, user=request.user)

            # Update the income entry with new data
            income.amount = float(amount)
            income.category = category
            income.description = description
            income.date = timezone.now()  # Optionally update the date to the current timestamp
            income.save()

            # Return success response for AJAX request
            return JsonResponse({'success': True, 'message': 'Income updated successfully!', 'id': income.id})

        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Failed to find the specified category.'}, status=400)

        except Exception as e:
            # If something goes wrong, return an error response
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

    # For GET requests, render the form to edit income
    return render(request, 'tracker/edit_income.html', {
        'income': income,  # Pass the income entry for pre-filling the form
        'categories': categories
    })



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Income

@login_required
def delete_income(request, income_id):
    try:
        # Fetch income entry to delete and ensure it belongs to the logged-in user
        income = get_object_or_404(Income, id=income_id, user=request.user)

        # Delete the income entry
        income.delete()

        # Return success response
        return JsonResponse({'success': True, 'message': 'Income deleted successfully!'})

    except Income.DoesNotExist:
        # Return error response if income is not found
        return JsonResponse({'success': False, 'message': 'Income not found or you do not have permission to delete it.'}, status=400)

    except Exception as e:
        # Handle any unexpected errors
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Expense, Category
from .forms import ExpenseForm  # Assuming you have a form for expenses

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        try:
            # Parse data from the form
            amount = request.POST.get('amount')
            category_id = request.POST.get('category')
            description = request.POST.get('description', '')
            category_name = request.POST.get('category_name', None)

            if not amount or not category_id:
                return JsonResponse({'success': False, 'message': 'Amount and category are required fields.'}, status=400)

            # If 'new' category is selected, create it
            if category_id == 'new':
                if not category_name:
                    return JsonResponse({'success': False, 'message': 'Category name is required to create a new category.'}, status=400)
                category = Category.objects.create(name=category_name, user=request.user, type='expense')
            else:
                category = get_object_or_404(Category, id=category_id, user=request.user)

            # Update the expense
            expense.amount = float(amount)
            expense.category = category
            expense.description = description
            expense.date = timezone.now()
            expense.save()

            return JsonResponse({'success': True, 'message': 'Expense updated successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

    # Render the form with existing expense details
    return render(request, 'edit_expense.html', {'expense': expense, 'categories': categories})


@login_required
def delete_expense(request, expense_id):
    if request.method == 'POST':
        try:
            expense = get_object_or_404(Expense, id=expense_id, user=request.user)
            expense.delete()
            return JsonResponse({'success': True, 'message': 'Expense deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
