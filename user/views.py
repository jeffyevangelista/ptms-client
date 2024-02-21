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
            if user is not None:
                login(request, user)

                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'message': 'User login successful.',
                    'token': token.key,
                    'role': user.role 
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email or Password not found.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def current_user(request):
    serializer = user_Serializer(request.user) 
    return Response(serializer.data)
