from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RequestForm_Serializer , Request_Serializer
from django.http import JsonResponse
from .models import RequestForm
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from .models import RequestForm
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


class RequestForm_view(ModelViewSet):
    serializer_class = RequestForm_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class LatestVoucherView(View):
    def get(self, request, *args, **kwargs):
        latest_voucher = RequestForm.objects.order_by('-id').first()
        latest_voucher_number = latest_voucher.voucher_no if latest_voucher else None
        return JsonResponse({'latest_voucher_number': latest_voucher_number})
    


def create_request_form(request):
    try:
        serializer = Request_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class FormListAPIView(generics.ListAPIView):

    serializer_class = RequestForm_Serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['activity', 'descriptions', 'voucher_no']


    def get_queryset(self):
        user = self.request.user
        token = self.request.auth  
        print(f"User: {user}, Token: {token}")

        # Inspect authentication classes
        authentication_classes = getattr(self, 'authentication_classes', [])
        print(f"Authentication Classes: {authentication_classes}")

        if user.is_authenticated and user.business_unit:
            print(f"User {user.email} is logged in.")
            return RequestForm.objects.filter(business_unit=user.business_unit)
        else:
            print("User is not logged in.")
            return RequestForm.objects.all()
