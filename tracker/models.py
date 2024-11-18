from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
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
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories')

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'income'})
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category}"


class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'expense'})
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category}"


class EMI(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    frequency = models.CharField(max_length=10, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'type': 'emi'})
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} - Due on {self.due_date} - {'Paid' if self.status else 'Unpaid'}"

