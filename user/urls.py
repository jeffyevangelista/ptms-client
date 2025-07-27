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
    path('api/custodian_users/', views.custodian_users, name='custodian_users'),
    path('api/check_business_unit_based_on_email/', views.check_business_unit_based_on_email, name='check_business_unit_based_on_email'),
    path('logout/', views.logout_view, name='logout'),


]
