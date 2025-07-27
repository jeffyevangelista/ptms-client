from django.db import models
from user.models import User
from businessUnit.models import BusinessUnit
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Fund(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.amount} '
    
@receiver(post_save, sender=Fund)
def create_fund_log(sender, instance, created, **kwargs):
    if created:
        FundLog.objects.create(
            fund=instance,
            name=instance.name,
            amount=instance.amount,
            user=instance.user
        )

class FundLog(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.amount} by {self.user} at {self.timestamp}'
    
class BusinessUnitInFund(models.Model):
    fund_name = models.ForeignKey(Fund, on_delete=models.CASCADE)
    business_units = models.ManyToManyField(BusinessUnit)

    def __str__(self):
        return f'{self.fund_name} - {self.business_units} '
    