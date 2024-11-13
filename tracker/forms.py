from django import forms
from django.contrib.auth.models import User
from .models import Income, Expense, EMI, Category

# RegisterForm for user registration
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# IncomeForm for adding income
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']

# ExpenseForm for adding expense
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'description']

# EMIForm for adding EMI
class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['amount', 'due_date', 'frequency', 'category', 'description']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input widget
        }

# CategoryForm for adding categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
