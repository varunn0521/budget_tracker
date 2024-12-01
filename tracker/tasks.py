from celery import shared_task
from .models import EMI, Income
from datetime import date, timedelta

@shared_task
def process_emis():
    today = date.today()
    emis = EMI.objects.filter(due_date__lte=today, status="active")
    for emi in emis:
        try:
            # Assuming user has a linked income
            user_income = Income.objects.get(user=emi.user)
            if user_income.amount >= emi.amount:
                # Deduct EMI amount
                user_income.amount -= emi.amount
                user_income.save()

                # Update EMI details
                emi.remaining_installments -= 1
                emi.due_date += timedelta(days=get_days_for_frequency(emi.frequency))
                if emi.remaining_installments == 0:
                    emi.status = "completed"
                emi.save()
            else:
                emi.status = "defaulted"
                emi.save()
        except Income.DoesNotExist:
            emi.status = "defaulted"
            emi.save()

def get_days_for_frequency(frequency):
    mapping = {
        'daily': 1,
        'weekly': 7,
        'bi-weekly': 14,
        'monthly': 30,
        'quarterly': 90,
        'yearly': 365,
    }
    return mapping.get(frequency, 30)
