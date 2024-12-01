from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Income, Expense, EMI, Category
import re
from django.forms import ValidationError
from django.http import JsonResponse


# Custom User Creation Form
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password']  

    # Validate password based on custom conditions
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        
        # Check for length of password
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        # Check for special characters
        if not re.search(r'[\W_]', password):
            raise forms.ValidationError('Password must contain at least one symbol (e.g., !, @, #, $).')
        
        return password

# Register Form (using the CustomUser model)
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.username = user.email  

        user.backend = 'tracker.backend.EmailBackend'  

        if commit:
            user.save()
            Category.create_default_categories(user) 
        return user

# Login Form (using the email as username)
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Email"


from django import forms
from .models import Income, Category

class IncomeForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False, 
        label="Add New Category", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new category'})
    )

    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(type='income', user=self.user)

    def clean_new_category(self):
        new_category = self.cleaned_data.get('new_category')
        if new_category:
            new_category = new_category.strip()
            # Check if the new category already exists
            if Category.objects.filter(name=new_category, type='income', user=self.user).exists():
                raise forms.ValidationError("This category already exists.")
        return new_category

    def save(self, commit=True):
        income = super().save(commit=False)
        new_category = self.cleaned_data.get('new_category')

        if self.user:
            income.user = self.user  # Ensure income is associated with the logged-in user

        # Handle new category creation if provided
        if new_category:
            category, created = Category.objects.get_or_create(
                name=new_category.strip(), type='income', user=self.user
            )
            income.category = category

        # Save the income object
        if commit:
            income.save()
        return income



class ExpenseForm(forms.ModelForm):
    new_category = forms.CharField(required=False, label="Add New Category")

    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'description']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(type='expense', user=self.user)

    def save(self, commit=True):
        expense = super().save(commit=False)
        new_category = self.cleaned_data.get('new_category')

        if self.user:
            expense.user = self.user  # Ensure expense is associated with the logged-in user

        # Handle new category creation if provided
        if new_category:
            # Check if the category already exists for this user
            category, created = Category.objects.get_or_create(
                name=new_category.strip(), type='expense', user=self.user
            )
            expense.category = category

        # Save the expense object
        if commit:
            expense.save()
        return expense


class EMIForm(forms.ModelForm):
    new_category = forms.CharField(required=False, label="Add New Category")

    class Meta:
        model = EMI
        fields = ['amount', 'category', 'description', 'due_date', 'frequency', 'remaining_installments']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(type='emi', user=user)

    def save(self, commit=True):
        emi = super().save(commit=False)
        new_category = self.cleaned_data.get('new_category')

        if new_category:
            if Category.objects.filter(name=new_category, type='emi', user=emi.user).exists():
                raise ValidationError(f"Category '{new_category}' already exists.")
            category = Category.objects.create(
                name=new_category, type='emi', user=emi.user
            )
            emi.category = category

        if commit:
            emi.save()
        return emi

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        if category_name:
            new_category, created = Category.objects.get_or_create(name=category_name)
            if created:
                return JsonResponse({'success': True, 'id': new_category.id, 'name': new_category.name})
    return JsonResponse({'success': False}, status=400)
