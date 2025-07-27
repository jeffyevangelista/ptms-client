from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import user_Serializer
from django.contrib.auth import authenticate, login, logout
from .serializers import LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

#api for crud
class User_view(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user_Serializer


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        
    def update(self , request, *args, **kwargs):
        instance = self.get_object()
        password = request.data.get('password', None)
        
        serializer = self.get_object()
        password = request.data.get('password', None)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if password:
            instance.set_password(password)
            instance.save()
            
        return Response(serializer.data)
        

    
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                token, created = Token.objects.get_or_create(user=user)

                response_data = {
                    'message': 'User login successful.',
                    'token': token.key,
                    'role': user.role,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'id': user.id,
                }

                if user.business_unit.exists():
                    response_data['business_unit'] = {
                        'ids': list(user.business_unit.values_list('id', flat=True)),
                    }
                else:
                    response_data['business_unit'] = None

                return JsonResponse(response_data, status=status.HTTP_200_OK, encoder=DjangoJSONEncoder)
            else:
                return Response({'error': 'Email or Password not found.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def current_user(request):
    serializer = user_Serializer(request.user) 
    return Response(serializer.data)


@api_view(['GET'])
def custodian_users(request):
    if request.method == 'GET':
        custodian_users = User.objects.filter(role='Fund Custodian')
        serializer = user_Serializer(custodian_users, many=True)

        return Response(serializer.data)
    

@api_view(['POST'])
def check_business_unit_based_on_email(request):
    email = request.data.get('email', None)
    
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        business_units = list(user.business_unit.values_list('business_unit_name', flat=True))
        role = user.role
        
        return Response({'businessUnits': business_units,'role': role}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt  # Use for debugging, not recommended for production
def logout_view(request):
    if request.method == 'POST':
        try:
            logout(request)
            response = JsonResponse({"success": "Logged out"}, status=200)
            # Clear session cookies
            response.delete_cookie('sessionid')
            response.delete_cookie('csrftoken')
            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)