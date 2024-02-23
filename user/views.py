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
#api for crud
class User_view(ModelViewSet):
    serializer_class = user_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            print(f"User: {user}")
            if user is not None:
                print("User is authenticated and logging in.")
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

                if user.business_unit:
                    response_data['business_unit'] = {
                        'id': user.business_unit.id,
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

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User login Successfully.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Email or Password not found.')
    return render(request, 'User/login.html')