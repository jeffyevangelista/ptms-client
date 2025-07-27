from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'role', 'get_business_units')

    def get_business_units(self, obj):
        return ", ".join([bu.business_unit_name  for bu in obj.business_unit.all()])
    get_business_units.short_description = 'Business Units'