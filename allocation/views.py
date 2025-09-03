
from rest_framework.viewsets import ModelViewSet
from .serializers import allocation_Serializer,allocationLog_Serializer
from fund.models import Fund
from django.db import transaction
from .models import Allocation,AllocationLog
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class Allocation_view(ModelViewSet):
    serializer_class = allocation_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        associated_fund = instance.name
        associated_fund.amount += instance.amount
        associated_fund.save()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AllocationLog_view(ModelViewSet):
    serializer_class = allocationLog_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

@api_view(['POST'])
@transaction.atomic
def create_fund_allocation(request):
    if request.method == 'POST':
        serializer = allocation_Serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            business_unit = serializer.validated_data['business_unit']
            amount = serializer.validated_data['amount']

            if Allocation.objects.filter(name=name, business_unit=business_unit).exists():
                return Response({'message': 'Business unit already allocated for this fund.'}, status=status.HTTP_400_BAD_REQUEST)

            fund_instance = Fund.objects.get(pk=name.id)
            fund_instance.amount -= amount
            fund_instance.save()

            Allocation.objects.create(name=name, business_unit=business_unit, amount=amount)

            return Response({'message': 'Fund Allocation created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
@transaction.atomic
def edit_fund_allocation(request, fund_allocation_id):
    if request.method == 'PUT':
        serializer = allocation_Serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            business_unit = serializer.validated_data['business_unit']
            amount = serializer.validated_data['amount']

            try:
                fund_instance = Fund.objects.get(pk=name.id)
                allocation_instance = Allocation.objects.get(pk=fund_allocation_id)

                existing_allocation = Allocation.objects.filter(
                    name=name,
                    business_unit=business_unit
                ).exclude(pk=fund_allocation_id).first()

                if existing_allocation:
                    return Response(
                        {'message': 'Allocation for the specified fund and business unit already exists'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if allocation_instance.amount > amount:
                    difference = allocation_instance.amount - amount
                    fund_instance.amount += difference
                    fund_instance.save()

                elif allocation_instance.amount < amount:
                    difference = amount - allocation_instance.amount
                    fund_instance.amount -= difference
                    fund_instance.save()

                allocation_instance.amount = amount
                allocation_instance.business_unit = business_unit
                allocation_instance.save()

                return Response({'message': 'Fund Allocation updated successfully'}, status=status.HTTP_200_OK)

            except Fund.DoesNotExist or Allocation.DoesNotExist:
                return Response({'message': 'Fund or Allocation not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllocationListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_fund_name = user.fund_set.first().name if user.fund_set.exists() else None

            allocations = Allocation.objects.filter(name__name=user_fund_name)

            serializer = allocation_Serializer(allocations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class Allocation_List_Per_BU_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units = user.business_unit.all()

            if user_business_units:
                business_units_data = []

                for user_business_unit in user_business_units:
                    allocations = Allocation.objects.filter(business_unit=user_business_unit)
                    for allocation in allocations:
                        business_unit_data = {
                            'id': allocation.id,
                            'business_unit_name': allocation.business_unit.business_unit_name,
                            'business_unit_id': allocation.business_unit.id,
                            'allocated_amount': allocation.amount
                        }
                        business_units_data.append(business_unit_data)

                return Response(business_units_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


class Allocation_Log_Per_BU_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            # Get the fund associated with the user
            fund_for_user = Fund.objects.filter(user=user).first()

            if fund_for_user:
                # Filter allocation logs related to the fund
                allocation_logs = AllocationLog.objects.filter(allocation__name=fund_for_user)

                allocation_logs_data = []

                for log in allocation_logs:
                    log_data = {
                        'id': log.id,
                        'business_unit_name': log.business_unit,
                        'allocation_name': log.name,
                        'amount': log.amount
                    }
                    allocation_logs_data.append(log_data)
                return Response(allocation_logs_data, status=status.HTTP_200_OK)
            else:
                error_message = "No fund associated with the user."
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message = "User is not authenticated."
            return Response({"error": error_message}, status=status.HTTP_401_UNAUTHORIZED)

