from django.db import models
from fund.models import Fund
from user.models import User
# Create your models here.
class BusinessUnit(models.Model):
    business_unit_name = models.CharField(max_length = 100)
    fund = models.ForeignKey(Fund,on_delete=models.CASCADE)

    def __str__(self):
        return self.business_unit_name
    
class UserCompanyRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_BusinessUnit_relationships')
    businessUnit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='user_BusinessUnit_relationships')

    def __str__(self):
        return f'{self.user} - {self.businessUnit}'