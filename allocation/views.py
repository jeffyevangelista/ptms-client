from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import allocation_Serializer
from django.http import JsonResponse
from fund.models import Fund
from django.db import transaction
from .models import Allocation
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


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


class AllocationListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_fund_name = user.fund_set.first().name if user.fund_set.exists() else None

            allocations = Allocation.objects.filter(name__name=user_fund_name)
            print(allocations)

            serializer = allocation_Serializer(allocations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class Allocation_List_Per_BU_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_unit = user.business_unit 

            if user_business_unit:
                allocations = Allocation.objects.filter(business_unit=user_business_unit)
                business_units_data = []

                for allocation in allocations:
                    business_unit_data = {
                        'id': allocation.id,
                        'business_unit_name': allocation.business_unit.business_unit_name,
                        'allocated_amount': allocation.amount
                    }
                    business_units_data.append(business_unit_data)

                return Response(business_units_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)