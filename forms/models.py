from django.db import models
from businessUnit.models import BusinessUnit
from allocation.models import Allocation
from user.models import User
from django.utils import timezone
from fund.models import Fund

class RequestForm(models.Model):

    def generate_reference_code(self):
        latest_voucher_no = RequestForm.objects.filter(business_unit=self.business_unit).order_by('-id').first()
        if latest_voucher_no:
            last_code = latest_voucher_no.voucher_no
            base_code, numeric_part = last_code.rsplit('-', 1)
            numeric_part = int(numeric_part) + 1
            new_code = f"{base_code}-{numeric_part:05d}"
        else:
            new_code = f"PR-1"

        return new_code
    
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Released', 'Released'),
        ('Liquidated', 'Liquidated'),
        ('Declined', 'Declined'),
        ('Replenished', 'Replenished'),
        ('Cancel', 'Cancel'),
    ]

    voucher_no = models.CharField(max_length=15,default=generate_reference_code)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    fund_allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, default=None)
    activity = models.CharField(max_length=50)
    profit_center = models.CharField(max_length=50)
    covered_from = models.DateField(default=timezone.now)
    covered_to = models.DateField()
    date_requested = models.DateField(blank=True, null=True)

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='Pending',null=True, blank=True)
    excess = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    refund = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    encoded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encoder' ,null=True, blank=True)
    requested_by = models.CharField(max_length=50 , null=True, blank=True)
    encoded_date = models.DateField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cost_controller' ,null=True, blank=True)
    reviewed_date = models.DateField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='general_manager',null=True, blank=True)
    approved_date = models.DateField(blank=True, null=True)
    release_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custodian',null=True, blank=True)
    released_date = models.DateField(blank=True, null=True)
    received_by = models.CharField(max_length=50, null=True, blank=True)
    received_date = models.DateField(blank=True, null=True)

    liquidated_date = models.DateField(blank=True, null=True)
    replenish_date = models.DateField(blank=True, null=True) 

    with_receipt = models.DecimalField(max_digits=15, decimal_places=2, default=None, null=True)
    with_out_receipt = models.DecimalField(max_digits=15, decimal_places=2, default=None, null=True)

    def __str__(self):
        return str(self.voucher_no)
    def save(self, *args, **kwargs):
        if not self.voucher_no:
            self.voucher_no = self.generate_reference_code()
        super().save(*args, **kwargs)
    
    
class Item(models.Model):
    request_form = models.ForeignKey(RequestForm, related_name='items', on_delete=models.CASCADE)
    descriptions = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    uom = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    item_total_amount = models.DecimalField(max_digits=15, decimal_places=2,default=None, null=True)
    
    



