from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationFomr(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'user_cc', 'email')
        
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFomr
    model = User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
                'fields': (
                    'username',
                    'user_cc',
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_superuser',
                    'is_active'
                )
            }
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Aditional Infortmation', {'fields': ('user_cc',)}),
    )
    list_display = ('username', 'email', 'user_cc', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'user_cc', 'email')
    
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Career)
admin.site.register(CareerPeriodPricing)
admin.site.register(FinancingRequest)
admin.site.register(Installment)