from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RequestForm_Serializer,Item_Serializer,UpdateRequestForm_Serializer,editRequestForm_Serializer
from django.http import JsonResponse
from .models import RequestForm
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RequestForm
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from fund.models import Fund, BusinessUnitInFund
from allocation.models import Allocation
from django.db import transaction
import copy
from .models import Item
from allocation.models import AllocationLog
from allocation.serializers import allocation_Serializer, allocationLog_Serializer
from datetime import date

class RequestForm_view(ModelViewSet):
    serializer_class = UpdateRequestForm_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class Item_view(ModelViewSet):
    serializer_class = Item_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

class LatestVoucherView(View):
    def get(self, request, *args, **kwargs):
        all_vouchers = RequestForm.objects.order_by('-id')

        vouchers_data = []

        for voucher in all_vouchers:
            voucher_data = {
                'voucher_number': voucher.voucher_no,
                'business_unit': {},
            }

            if voucher.business_unit:
                voucher_data['business_unit'] = {
                    'id': voucher.business_unit.id,
                    'name': voucher.business_unit.business_unit_name,
                }

            vouchers_data.append(voucher_data)
        response_data = {
            'vouchers': vouchers_data
        }
        return JsonResponse(response_data)

@api_view(['POST'])
def create_request_form(request):
    if request.method == 'POST':
        serializer = RequestForm_Serializer(data=request.data)
        
        if serializer.is_valid():
            request_form = serializer.save()
            return Response({'message': 'RequestForm created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@transaction.atomic
def edit_request_form(request, pk):
    try:
        request_form = RequestForm.objects.get(pk=pk)
    except RequestForm.DoesNotExist:
        return Response({'message': 'RequestForm not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':

        serializer = editRequestForm_Serializer(request_form, data=request.data)

        if serializer.is_valid():
            serializer.save()
            items_data = request.data.get('items', [])
            request_form.items.all().delete()
            for item_data in items_data:
                Item.objects.create(request_form=request_form, **item_data)

            return Response({'message': 'RequestForm edited successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PurchaseRequestListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None
      
        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:
                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids,approved_by__isnull=True )
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class PurchaseRequestApprovedListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:
                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, reviewed_by__isnull=False,approved_by__isnull=False, status='Approved' )
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
class PurchaseRequestReleasedListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:
                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, reviewed_by__isnull=False,approved_by__isnull=False, status='Released' )
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class PurchaseRequest_Reviewer_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_unit = user.business_unit
            
            if user_business_unit:
                request_form = RequestForm.objects.filter(business_unit=user_business_unit, reviewed_by=None)
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        

class PurchaseRequest_GeneralManager_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:

                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, reviewed_by__isnull=False, approved_by=None,status='Approved' )
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['PUT'])
@transaction.atomic
def Fund_Custodian_Release_Amount(request, pk):
    try:
        request_form = RequestForm.objects.get(pk=pk)
    except RequestForm.DoesNotExist:
        return Response({'message': 'RequestForm not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UpdateRequestForm_Serializer(request_form, data=request.data)

        if serializer.is_valid():
            request_form_copy = serializer.save()


            if request_form.fund_allocation:
                allocation = request_form.fund_allocation
                allocation.amount -= request_form.amount
                allocation.save()


            return Response({'message': 'RequestForm edited successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class Cost_Controller_To_Be_Release_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_funds = Fund.objects.filter(user=user)

            business_units_in_funds = BusinessUnitInFund.objects.filter(fund_name__in=user_funds)

            allocations = Allocation.objects.filter(business_unit__in=business_units_in_funds.values('business_units'))

            request_form = RequestForm.objects.filter(
                fund_allocation__in=allocations,
                business_unit__in=business_units_in_funds.values('business_units'),
                approved_by__isnull=False,
                release_by__isnull=True,
                status='Approved'
            )

            serializer = RequestForm_Serializer(request_form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class Cost_Controller_Release_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_funds = Fund.objects.filter(user=user)

            business_units_in_funds = BusinessUnitInFund.objects.filter(fund_name__in=user_funds)

            allocations = Allocation.objects.filter(business_unit__in=business_units_in_funds.values('business_units'))

            request_form = RequestForm.objects.filter(
                fund_allocation__in=allocations,
                business_unit__in=business_units_in_funds.values('business_units'),
                approved_by__isnull=False,
                release_by__isnull=False,
                status='Released'
            )

            serializer = RequestForm_Serializer(request_form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class Cost_Controller_Liquidated_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_funds = Fund.objects.filter(user=user)

            business_units_in_funds = BusinessUnitInFund.objects.filter(fund_name__in=user_funds)

            allocations = Allocation.objects.filter(business_unit__in=business_units_in_funds.values('business_units'))

            request_form = RequestForm.objects.filter(
                fund_allocation__in=allocations,
                business_unit__in=business_units_in_funds.values('business_units'),
                approved_by__isnull=False,
                release_by__isnull=False,
                status='Liquidated'
            )

            serializer = RequestForm_Serializer(request_form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


class Cost_Controller_Replenish_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:
                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, reviewed_by__isnull=False,approved_by__isnull=False, status='Replenished' )
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@transaction.atomic
def replenish_function(request, pk):
    if request.method == 'PUT':
        try:
            request_form_instance = RequestForm.objects.get(pk=pk)
        except RequestForm.DoesNotExist:
            return Response({'message': 'Purchase request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateRequestForm_Serializer(request_form_instance, data=request.data)
        if serializer.is_valid():
            request_form = serializer.save()

            
            update_allocation_amount(request_form)
            
            return Response({'message': 'Purchase request updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def update_allocation_amount(request_form):
    if request_form.fund_allocation:
        allocation = request_form.fund_allocation
        allocation.amount += request_form.amount
        allocation.save()

#Encoder Decline
class PurchaseRequest_Decline_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:
                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, status__in=['Declined', 'Cancel'])
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have any associated business units."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
#Encoder Approved
class PurchaseRequest_Approved_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:
                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, reviewed_by__isnull=False, approved_by__isnull=False, status='Approved')
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['PUT'])
@transaction.atomic
def decline_return_fund_function(request, pk):
    if request.method == 'PUT':
        try:
            request_form_instance = RequestForm.objects.get(pk=pk)
        except RequestForm.DoesNotExist:
            return Response({'message': 'Purchase request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateRequestForm_Serializer(request_form_instance, data=request.data)
        if serializer.is_valid():
            request_form = serializer.save()

            
            return Response({'message': 'Purchase request updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def admin_released(request):
    try:
        queryset = RequestForm.objects.filter(status='Released')
        serializer = UpdateRequestForm_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def admin_liquidated(request):
    try:
        queryset = RequestForm.objects.filter(status='Liquidated')
        serializer = UpdateRequestForm_Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class Fund_Custodian_Pie_Chart(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_funds = Fund.objects.filter(user=user)

            business_units_in_funds = BusinessUnitInFund.objects.filter(fund_name__in=user_funds)

            allocations = Allocation.objects.filter(business_unit__in=business_units_in_funds.values('business_units'))

            request_form = RequestForm.objects.filter(
                fund_allocation__in=allocations,
                business_unit__in=business_units_in_funds.values('business_units'),
                approved_by__isnull=False,
                release_by__isnull=False
            )

            serializer = RequestForm_Serializer(request_form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        


class Encoder_Liquidated_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_units_ids = user.business_unit.values_list('id', flat=True)
            
            if user_business_units_ids:

                request_form = RequestForm.objects.filter(business_unit__in=user_business_units_ids, status='Liquidated' )
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
        

@api_view(['PUT'])
@transaction.atomic
def excess_or_refund_function(request, pk):
    if request.method == 'PUT':
        try:
            request_form_instance = RequestForm.objects.get(pk=pk)
        except RequestForm.DoesNotExist:
            return Response({'message': 'Purchase request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateRequestForm_Serializer(request_form_instance, data=request.data)
        if serializer.is_valid():
            request_form = serializer.save()


            if request_form.excess:
                request_form.amount -= request_form.excess
                updated_allocation_amount(request_form.fund_allocation, request_form.excess)
                request_form.save()

            if request_form.refund:
                request_form.amount += request_form.refund
                updated_allocation_amount(request_form.fund_allocation, -request_form.refund)
                request_form.save()
            

            return Response({'message': 'Purchase request updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def updated_allocation_amount(allocation, amount):
    if allocation:
        allocation.amount += amount
        allocation.save()


class Fund_Manager_Reports_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            # Get today's date
            today_date = date.today()

            user_funds = Fund.objects.filter(user=user)

            business_units_in_funds = BusinessUnitInFund.objects.filter(fund_name__in=user_funds)

            allocations = Allocation.objects.filter(business_unit__in=business_units_in_funds.values('business_units'))

            allocation_logs = AllocationLog.objects.filter(allocation__in=allocations)

            request_form = RequestForm.objects.filter(
                fund_allocation__in=allocations,
                business_unit__in=business_units_in_funds.values('business_units'),
                status__in=['Released', 'Liquidated', 'Replenished'],
            )
                

            request_form_serializer = RequestForm_Serializer(request_form, many=True)
            allocation_serializer = allocation_Serializer(allocations, many=True)
            allocation_log_serializer = allocationLog_Serializer(allocation_logs, many=True)

            response_data = {
                'request_forms': request_form_serializer.data,
                'allocations': allocation_serializer.data,
                'allocation_logs': allocation_log_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
    
class Fund_Manager_Daily_Reports_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            # Get today's date
            today_date = date.today()

            user_funds = Fund.objects.filter(user=user)

            business_units_in_funds = BusinessUnitInFund.objects.filter(fund_name__in=user_funds)

            allocations = Allocation.objects.filter(business_unit__in=business_units_in_funds.values('business_units'))

            allocation_logs = AllocationLog.objects.filter(allocation__in=allocations)

            # Filter request forms based on release date
            request_form = RequestForm.objects.filter(
                fund_allocation__in=allocations,
                business_unit__in=business_units_in_funds.values('business_units'),
                status__in=['Released', 'Liquidated', 'Replenished'],
            )

            request_form_serializer = RequestForm_Serializer(request_form, many=True)
            allocation_serializer = allocation_Serializer(allocations, many=True)
            allocation_log_serializer = allocationLog_Serializer(allocation_logs, many=True)

            response_data = {
                'request_forms': request_form_serializer.data,
                'allocations': allocation_serializer.data,
                'allocation_logs': allocation_log_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
