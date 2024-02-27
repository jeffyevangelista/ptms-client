from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RequestForm_Serializer
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
class RequestForm_view(ModelViewSet):
    serializer_class = RequestForm_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class LatestVoucherView(View):
    def get(self, request, *args, **kwargs):
        latest_voucher = RequestForm.objects.order_by('-id').first()
        latest_voucher_number = latest_voucher.voucher_no if latest_voucher else None
        return JsonResponse({'latest_voucher_number': latest_voucher_number})
    
    
class PurchaseRequestListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_unit = user.business_unit
            
            if user_business_unit:
                request_form = RequestForm.objects.filter(business_unit=user_business_unit)
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("User does not have a business unit.")
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class PurchaseRequest_Reviewer_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_unit = user.business_unit
            
            if user_business_unit:
                # Filter based on the condition where reviewed_by is null
                request_form = RequestForm.objects.filter(business_unit=user_business_unit, reviewed_by=None)
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("User does not have a business unit.")
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class PurchaseRequest_GeneralManager_List_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_business_unit = user.business_unit
            
            if user_business_unit:
                # Filter based on the condition where reviewed_by is null
                request_form = RequestForm.objects.filter(business_unit=user_business_unit, reviewed_by__isnull=False, approved_by=None)
                serializer = RequestForm_Serializer(request_form, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("User does not have a business unit.")
                return Response({"error": "User does not have a business unit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
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
                release_by__isnull=False
            )

            serializer = RequestForm_Serializer(request_form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("User is not authenticated.")
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
                release_by__isnull=True
            )

            serializer = RequestForm_Serializer(request_form, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)