from django.db import models, transaction
from businessUnit.models import BusinessUnit
from allocation.models import Allocation
from user.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class RequestForm(models.Model):

    def generate_reference_code():

        latest_voucher_no = RequestForm.objects.order_by('-id').first()
        if latest_voucher_no:
            last_code = latest_voucher_no.voucher_no
            base_code, numeric_part = last_code.rsplit('-', 1)
            numeric_part = int(numeric_part) + 1
            new_code = f"{base_code}-{numeric_part:05d}"
        else:
            new_code = f"PR-00000"

        return new_code
    voucher_no = models.CharField(max_length=15,default=generate_reference_code, unique=True)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    fund_allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, default=None)
    activity = models.CharField(max_length=50)
    profit_center = models.CharField(max_length=50)
    covered_from = models.DateField(default=timezone.now)
    covered_to = models.DateField()
    date_requested = models.DateField()

    descriptions = models.CharField(max_length=50)
    quantity = models.IntegerField()
    uom = models.CharField(max_length=50)
    price = models.IntegerField()
    amount = models.IntegerField()

    encoded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encoder' ,null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cost_controller' ,null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='general_manager',null=True)
    release_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custodian',null=True)

    def __str__(self):
        return str(self.voucher_no)
    
    def deduct_amount_from_allocation(self):
        print(f"Allocation ID:, Allocation amount: {self.fund_allocation.amount}, Requested amount: {self.amount}")
        if self.fund_allocation.amount < self.amount:
            raise ValidationError("Insufficient allocated funds.")
        self.fund_allocation.amount -= self.amount
        self.fund_allocation.save()

    @transaction.atomic
    def save(self, *args, **kwargs):
        print(f"After deduction - Allocation amount: {self.fund_allocation.amount}, Requested amount: {self.amount}")
        self.deduct_amount_from_allocation()
        super().save(*args, **kwargs)
    



