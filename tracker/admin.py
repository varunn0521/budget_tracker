from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Income, Expense  # Import the Expense model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'category', 'date')  # Display columns for Income
    search_fields = ('category',)  # Search by category or another field
    ordering = ('-date',)  # Order by date, descending (most recent first)
    list_filter = ('date',)  # Filter by date

admin.site.register(Income, IncomeAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'category', 'date')  # Adjust to match your Expense model fields
    search_fields = ('category',)  # Search by category or another field
    ordering = ('-date',)  # Order by date, descending (most recent first)
    list_filter = ('date',)  # Filter by date

admin.site.register(Expense, ExpenseAdmin)
