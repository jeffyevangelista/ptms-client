from django.urls import path,include
from . import views

from .views import (
    User_view,LoginAPIView
)

urlpatterns = [
    path('',include([
        path('', User_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', User_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),

    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/current_user/', views.current_user, name='current_user'),

    path('login_user/', views.login_user, name='login_user'),

]