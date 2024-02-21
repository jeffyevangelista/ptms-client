from django.db import models
# Create your models here.
class BusinessUnit(models.Model):
    business_unit_name = models.CharField(max_length = 100)

    def __str__(self):
        return f'{self.business_unit_name}'
    
