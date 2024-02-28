from django.db import models
from user.models import User
from businessUnit.models import BusinessUnit
# Create your models here.
class Fund(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.amount} '
    
class BusinessUnitInFund(models.Model):
    fund_name = models.ForeignKey(Fund, on_delete=models.CASCADE)
    business_units = models.ManyToManyField(BusinessUnit)

    def __str__(self):
        return f'{self.fund_name} - {self.business_units} '
    
class Return_fund(models.Model):
    fund_name = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.fund_name} - {self.amount}'