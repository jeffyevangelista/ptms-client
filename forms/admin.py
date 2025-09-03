from django.contrib import admin
from .models import RequestForm
# Register your models here.
@admin.register(RequestForm)
class RequestFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'voucher_no', 'business_unit', 'activity')