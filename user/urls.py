from django.urls import path,include
from . import views

from .views import (
    User_view,login_user,dashboard
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

    path('login_user/', login_user, name='login_user'),
    path('dashboard/', dashboard, name='dashboard'),
]