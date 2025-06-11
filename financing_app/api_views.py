from decimal import Decimal
from rest_framework import status
from .models import FinancingRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class FinancingRequestAPIViews(APIView):
    
    def get(self, request, pk):
        appli = get_object_or_404(FinancingRequest, pk=pk)
        
        total_value = Decimal(appli.tuition_fee_with_discount)
        initial_fee = appli.down_payment
        interest_rate = appli.interest_rate
        admin_fee = appli.administration_fee
        num_fee = appli.number_installments
        
        financing_value = total_value - Decimal(initial_fee)
        
        total_interest = financing_value * Decimal(interest_rate / 100) * Decimal(num_fee)
        
        base_fee = (financing_value + interest_rate) / Decimal(num_fee)
        
        monthly_fee = base_fee * (1 + Decimal(admin_fee / 100))
        
        summary = {
            "student": str(appli.student),
            "career": appli.tuition_value.career.name,
            "period": appli.tuition_value.period,
            "tuition_value": float(total_value),
            "discount_applied": float(appli.discount_applied),
            "initial_fee": float(initial_fee),
            "financing_value": float(financing_value),
            "total_interest": float(total_interest, 2),
            "total_interest": round(float(total_interest), 2),
            "approx_monthly_fee": round(float(monthly_fee), 2),
            "number_fee": num_fee
        }
        
        return Response(summary, status=status.HTTP_200_OK)