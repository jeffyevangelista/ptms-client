from django.db import models
from businessUnit.models import BusinessUnit
from fund.models import Fund
# Create your models here.
class Allocation(models.Model):
    name = models.ForeignKey(Fund, on_delete=models.CASCADE)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
       return f'{self.business_unit.business_unit_name} Allocation'
    
