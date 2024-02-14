from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import user_Serializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#api for crud
class User_view(ModelViewSet):
    serializer_class = user_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

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
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')