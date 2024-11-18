from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Income, Expense, EMI, Category
import re

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


# Income Form
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(type='income', user=user)


# Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'description']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(type='expense', user=user)


# EMI Form
class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['amount', 'due_date', 'frequency', 'category', 'description']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(type='emi', user=user)
