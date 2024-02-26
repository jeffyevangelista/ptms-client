from django.db import models
from businessUnit.models import BusinessUnit
from fund.models import Fund
from django.core.exceptions import ValidationError
# Create your models here.
class Allocation(models.Model):
    name = models.ForeignKey(Fund, on_delete=models.CASCADE)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
       return f'{self.business_unit.business_unit_name} Allocation'
    
    def deduct_amount_from_fund(self):
        if self.name.amount < self.amount:
            raise ValidationError("Insufficient funds.")
        self.name.amount -= self.amount
        self.name.save()

    def save(self, *args, **kwargs):
        self.deduct_amount_from_fund()
        super().save(*args, **kwargs)