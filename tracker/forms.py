from django import forms
from django.contrib.auth.models import User
from .models import Income, Expense, EMI, Category

# RegisterForm for user registration
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# IncomeForm for adding income
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Calendar picker for date input
        }

    # Dynamically filter categories based on logged-in user
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter income categories for the logged-in user
            self.fields['category'].queryset = Category.objects.filter(type='income', user=user)
        self.fields['category'].empty_label = "Select Category"
        self.fields['amount'].required = True
        self.fields['date'].required = True
        self.fields['category'].required = True
        self.fields['description'].required = True

# ExpenseForm for adding expense
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'description']

    # Dynamically filter categories based on logged-in user
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter expense categories for the logged-in user
            self.fields['category'].queryset = Category.objects.filter(type='expense', user=user)
        self.fields['category'].empty_label = "Select Category"
        self.fields['amount'].required = True
        self.fields['date'].required = True
        self.fields['category'].required = True
        self.fields['description'].required = True

# EMIForm for adding EMI
class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['amount', 'due_date', 'frequency', 'category', 'description']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
        }

    # Dynamically filter categories based on logged-in user
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter expense categories for the logged-in user (assuming EMI uses expense categories)
            self.fields['category'].queryset = Category.objects.filter(type='expense', user=user)
        self.fields['category'].empty_label = "Select Category"
        self.fields['amount'].required = True
        self.fields['due_date'].required = True
        self.fields['frequency'].required = True
        self.fields['category'].required = True
        self.fields['description'].required = True

# CategoryForm for adding categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']

    # Dynamically set the category type options based on the logged-in user
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show categories that belong to the logged-in user
            self.fields['type'].queryset = Category.objects.filter(user=user)
        self.fields['type'].empty_label = "Select Category Type"
        self.fields['name'].required = True
        self.fields['type'].required = True
