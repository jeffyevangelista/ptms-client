from django.contrib import admin
from .models import Allocation, AllocationLog
# Register your models here.
@admin.register(Allocation)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_unit', 'amount')

@admin.register(AllocationLog)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'allocation', 'created_at', 'name', 'business_unit', 'amount')


