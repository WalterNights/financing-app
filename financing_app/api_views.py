from .models import *
from decimal import Decimal
from rest_framework import status
from .utils import calculator_fees
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class FinancingRequestAPIViews(APIView):
    
    def get(self, request, pk):
        appli = get_object_or_404(FinancingRequest, pk=pk)
        fees = calculator_fees(appli)
        
        # Summary
        summary = {
            "student": str(appli.user),
            "career": appli.tuition_value.career.name,
            "period": appli.tuition_value.period,
            "tuition_value": float(appli.tuition_fee_with_discount),
            "discount_applied": float(appli.discount_applied),
            "initial_fee": float(appli.down_payment),
            "financing_value": float(appli.tuition_fee_with_discount - appli.down_payment),
            "interest_rate": float(appli.interest_rate),
            "admin_fee": float(appli.administration_fee),
            "number_fee": appli.number_fee,
            "fees": fees
        }
        
        return Response(summary, status=status.HTTP_200_OK)