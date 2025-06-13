from datetime import timedelta
from .models import Installment
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP

def calculator_fees(financing_request):
    total = Decimal(financing_request.tuition_fee_with_discount)
    down_payment = financing_request.down_payment
    interest = Decimal(financing_request.interest_rate / 100)
    admin_fee = Decimal(financing_request.administration_fee / 100)
    n = financing_request.number_fee
    
    balance = total - down_payment
    capital_payment = balance / n
    fees = []
    
    for i in range(1, n + 1):
        monthly_interest = balance * interest
        base_fee = capital_payment + monthly_interest
        total_fee = (base_fee * (1 + admin_fee)).quantize(Decimal('0.01')), rounding=ROUND_HALF_UP 
        expiration = timezone.now().date() + timedelta(days=30 * i)
        
        fees.append({
            'num_fee': i,
            'valor_fee': float(total_fee),
            'expiration_date': expiration,
            'capital_payment': capital_payment,
            'interest': float(monthly_interest),
            'remaining_balance': float(max(balance - capital_payment, 0)),
        })
        
        balance -= capital_payment
        
    return fees


def generator_fees(financing_request):
    fees = calculator_fees(financing_request)
    installments = [
        Installment(
            financing_request = financing_request,
            num_fee = fee["num_fee"],
            valor_fee = fee["valor_fee"],
            expiration_date = fee["expiration_date"]
        )
        for fee in fees
    ]
    Installment.objects.bulk_create(installments)
    

def update_overdue_fee(arrears_percentage):
    today = timezone.now().date()
    fees = Installment.objects.filter(status="Pending", expiration_date__lt=today)
    for fee in fees:
        fee.arrears_calculate(arrears_percentage)