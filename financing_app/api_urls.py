from django.urls import path
from .api_views import FinancingRequestAPIViews

urlpatterns = [
    path('financing-request/<int:pk>/summary/', FinancingRequestAPIViews.as_view(), name='financing-summary')
]