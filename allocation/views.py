from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import allocation_Serializer
from django.http import JsonResponse
from fund.models import Fund
from django.db import transaction
from .models import Allocation
#api for crud
class Allocation_view(ModelViewSet):
    serializer_class = allocation_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    



@transaction.atomic
def create_fund_allocation(request):
    if request.method == 'POST':
        allocation_data = request.POST 
        allocation = Allocation.objects.create(
            name_id=allocation_data['name'],
            business_unit_id=allocation_data['business_unit'],
            amount=allocation_data['amount']
        )
        fund = Fund.objects.get(id=allocation_data['name'])
        fund.amount -= allocation.amount
        fund.save()

        return JsonResponse({'message': 'Fund Allocation created successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)