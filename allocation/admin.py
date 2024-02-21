from django.contrib import admin
from .models import Allocation
# Register your models here.
@admin.register(Allocation)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_unit', 'amount')


