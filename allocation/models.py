from django.db import models
from businessUnit.models import BusinessUnit
# Create your models here.
class Allocation(models.Model):
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.business_unit