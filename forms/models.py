from django.db import models
from businessUnit.models import BusinessUnit
from allocation.models import Allocation
from user.models import User
from django.utils import timezone
from fund.models import Fund

class RequestForm(models.Model):

    def generate_reference_code():

        latest_voucher_no = RequestForm.objects.order_by('-id').first()
        if latest_voucher_no:
            last_code = latest_voucher_no.voucher_no
            base_code, numeric_part = last_code.rsplit('-', 1)
            numeric_part = int(numeric_part) + 1
            new_code = f"{base_code}-{numeric_part:05d}"
        else:
            new_code = f"PR-000001"

        return new_code
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Released', 'Released'),
        ('Liquidated', 'Liquidated'),
        ('Declined', 'Declined'),
        ('Replenished', 'Replenished'),
    ]

    voucher_no = models.CharField(max_length=15,default=generate_reference_code, unique=True)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    fund_allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, default=None)
    activity = models.CharField(max_length=50)
    profit_center = models.CharField(max_length=50)
    covered_from = models.DateField(default=timezone.now)
    covered_to = models.DateField()
    date_requested = models.DateField(auto_now_add=True)

    amount = models.DecimalField(max_digits=15, decimal_places=0)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='Pending',null=True)

    encoded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encoder' ,null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cost_controller' ,null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='general_manager',null=True)
    release_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custodian',null=True)

    with_receipt = models.DecimalField(max_digits=15, decimal_places=0, default=None, null=True)
    with_out_receipt = models.DecimalField(max_digits=15, decimal_places=0, default=None, null=True)

    def __str__(self):
        return str(self.voucher_no)
    
class Item(models.Model):
    request_form = models.ForeignKey(RequestForm, related_name='items', on_delete=models.CASCADE)
    descriptions = models.CharField(max_length=50)
    quantity = models.IntegerField()
    uom = models.CharField(max_length=50)
    price = models.IntegerField()
    
class Refund(models.Model):
    voucher_no = models.ForeignKey(RequestForm, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=15, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
         return f'{self.voucher_no} - {self.refund_amount} '
    
class Excess(models.Model):
    voucher_no = models.ForeignKey(RequestForm, on_delete=models.CASCADE)
    excess_amount = models.DecimalField(max_digits=15, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
         return f'{self.voucher_no} - {self.excess_amount} '
    



