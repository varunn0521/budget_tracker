# tracker/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Category

# Signal to create default categories when a new user is created
@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:  
        # Define default categories for income and expense
        default_categories = [
            ('Salary', 'income'),
            ('Gift', 'income'),
            ('Food', 'expense'),
            ('Transportation', 'expense'),
            ('Entertainment', 'expense')
        ]
        
        for name, type in default_categories:
            # Check if the category already exists for the user
            if not Category.objects.filter(name=name, type=type, user=instance).exists():
                Category.objects.create(name=name, type=type, user=instance)
