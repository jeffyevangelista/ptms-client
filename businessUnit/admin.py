from django.contrib import admin

from .models import BusinessUnit
# Register your models here.
@admin.register(BusinessUnit)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_unit_name')


