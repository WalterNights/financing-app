from . import api_views
from django.urls import path

urlpatterns = [
    path('financing-request/<int:pk>/summary/', api_views.FinancingRequestAPIViews.as_view(), name='financing-summary')
]