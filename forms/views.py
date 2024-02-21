from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import RequestForm_Serializer
from django.http import JsonResponse
from .models import RequestForm
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

class RequestForm_view(ModelViewSet):
    serializer_class = RequestForm_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class LatestVoucherView(View):
    def get(self, request, *args, **kwargs):
        latest_voucher = RequestForm.objects.order_by('-id').first()
        latest_voucher_number = latest_voucher.voucher_no if latest_voucher else None
        return JsonResponse({'latest_voucher_number': latest_voucher_number})
    

@api_view(['POST'])
def create_request_form(request):
    try:
        current_user = request.user
        request.data['encoded_by'] = current_user.id
        serializer = RequestForm_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
