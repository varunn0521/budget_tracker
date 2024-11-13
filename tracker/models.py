from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')], default='expense')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'income'})
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'expense'})
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category}"

class EMI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    frequency = models.CharField(max_length=10, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'expense'})
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)  # False for unpaid, True for paid

    def __str__(self):
        return f"{self.amount} - Due on {self.due_date} - {'Paid' if self.status else 'Unpaid'}"
