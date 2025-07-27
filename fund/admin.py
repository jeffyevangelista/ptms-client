from django.contrib import admin
from .models import Fund
# Register your models here.
@admin.register(Fund)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'user')

