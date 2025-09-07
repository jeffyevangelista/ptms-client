
from rest_framework.viewsets import ModelViewSet
from .serializers import fund_Serializer, businessUnitInFund_Serializer,fundLog_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Fund
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from .models import BusinessUnitInFund
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

#api for crud
class Fund_view(ModelViewSet):
    serializer_class = fund_Serializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)     

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class FundLog_view(ModelViewSet):
    serializer_class = fundLog_Serializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
#api for crud
class BusinessUnitInFund_view(ModelViewSet):
    serializer_class = businessUnitInFund_Serializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
#Filter funds based on the user assigned in it
class FundListView(APIView):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        funds = Fund.objects.filter(user=request.user)
        serializer = fund_Serializer(funds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Filter business unit based on the fund
class Fund_Company_View(APIView):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # If User ↔ Fund is M2M, fund_set is correct.
        # If it's FK (Fund.user), swap the next line for Fund.objects.filter(user=request.user)
        fund_ids = list(request.user.fund_set.values_list('id', flat=True))
        if not fund_ids:
            return Response([], status=status.HTTP_200_OK)

        # Filter BusinessUnitInFund rows for ALL of the user’s funds
        business_units = (
            BusinessUnitInFund.objects
            .select_related('fund_name')   
            .filter(fund_name_id__in=fund_ids) 
            .order_by('id')
        )

        serializer = businessUnitInFund_Serializer(business_units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)