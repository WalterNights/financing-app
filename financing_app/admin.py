from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Aditional Infortmation', {'fields': ('rol', 'user_id')}),
    )

admin.site.register(Career)
admin.site.register(CareerPeriodPricing)
admin.site.register(FinancingRequest)