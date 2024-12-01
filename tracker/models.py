from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from datetime import date

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  

    objects = CustomUserManager()  

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('emi', 'EMI'),  
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('user', 'name', 'type') 

    def __str__(self):
        return f"{self.name} ({self.type})"

    @classmethod
    def create_default_categories(cls, user):
        default_income_categories = ['Salary', 'Bonus', 'Interest']
        default_expense_categories = ['Food', 'Travel', 'Bills']
        default_emi_categories = ['Loan', 'Mortgage', 'Car Loan']  

        for category_name in default_income_categories:
            cls.objects.create(name=category_name, type='income', user=user)

        for category_name in default_expense_categories:
            cls.objects.create(name=category_name, type='expense', user=user)

        for category_name in default_emi_categories:
            cls.objects.create(name=category_name, type='emi', user=user)

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'income'})
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category}"

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'expense'})
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category}"

from django.db import models
from datetime import date
from django.conf import settings

class EMI(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type': 'emi'}
    )
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(default=date.today)
    frequency = models.CharField(
        max_length=50,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ]
    )
    remaining_installments = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('defaulted', 'Defaulted'),
        ],
        default='active'
    )
    start_date = models.DateField(default=date.today)  # Add start date
    next_payment_date = models.DateField(default=date.today)  # Add next payment date

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.frequency})"
