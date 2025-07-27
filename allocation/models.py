from django.db import models
from businessUnit.models import BusinessUnit
from fund.models import Fund
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Allocation(models.Model):
    name = models.ForeignKey(Fund, on_delete=models.CASCADE)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
       return f'{self.business_unit.business_unit_name} - {self.name} Allocation'
    
class AllocationLog(models.Model):
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    business_unit = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.created_at}: {self.name} - {self.business_unit} Allocation'

@receiver(post_save, sender=Allocation)
def create_allocation_log(sender, instance, created, **kwargs):
    if created:
        AllocationLog.objects.create(
            allocation=instance,
            name=instance.name.name,
            business_unit=instance.business_unit.business_unit_name,
            amount=instance.amount
        )