
from rest_framework.viewsets import ModelViewSet
from .serializers import fund_Serializer, businessUnitInFund_Serializer,fundLog_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Fund
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from .models import BusinessUnitInFund

#api for crud
class Fund_view(ModelViewSet):
    serializer_class = fund_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class FundLog_view(ModelViewSet):
    serializer_class = fundLog_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
#api for crud
class BusinessUnitInFund_view(ModelViewSet):
    serializer_class = businessUnitInFund_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
    
    

    
#Filter funds based on the user assigned in it
class FundListView(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_id = user.id
            funds = Fund.objects.filter(user=user_id)
            serializer = fund_Serializer(funds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

#Filter business unit based on the fund
class Fund_Comapny_View(APIView):
    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        user = Token.objects.get(key=received_token).user if received_token else None

        if user and user.is_authenticated:
            user_fund_id = user.fund_set.first().id if user.fund_set.exists() else None
            business_units = BusinessUnitInFund.objects.filter(fund_name=user_fund_id)


            serializer = businessUnitInFund_Serializer(business_units, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        