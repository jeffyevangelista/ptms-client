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
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class RequestForm_view(ModelViewSet):
    serializer_class = RequestForm_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class LatestVoucherView(View):
    def get(self, request, *args, **kwargs):
        latest_voucher = RequestForm.objects.order_by('-id').first()
        latest_voucher_number = latest_voucher.voucher_no if latest_voucher else None
        return JsonResponse({'latest_voucher_number': latest_voucher_number})
    
    

